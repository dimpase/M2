#!/usr/bin/env python3
"""Audit declared M2 package dependencies without loading any packages.

Usage: check-package-dependencies.py [--edges] [package-directory [package ...]]
       check-package-dependencies.py --self-test

Requires NetworkX from PyPI (python -m pip install networkx==3.6.1).

Only literal PackageImports and PackageExports lists in newPackage headers are
accepted, plus the standard HomologicalAlgebraPackage alias. An unsupported
declaration is an error rather than a silent omission.
Body-level needsPackage/loadPackage/importFrom calls are outside this audit.
Exit status: 0 = acyclic, 1 = cycles, 2 = invalid or missing headers.
"""

import argparse
from collections import defaultdict
from pathlib import Path
import re
import sys

import networkx as nx


DEFAULT_PACKAGES = Path(__file__).resolve().parent.parent / "packages"
PACKAGE_NAME = re.compile(r"[A-Za-z0-9]+\Z")
TOKEN = re.compile(
    r'--[^\n]*|///[\s\S]*?///|"(?:\\.|[^"\\])*"|=>|[A-Za-z][A-Za-z0-9]*|[(){}\[\],]|\S'
)
OPEN = {"(": ")", "{": "}", "[": "]"}
# Set by M2/Macaulay2/m2/complexes.m2 in the standard M2 initialization.
PACKAGE_ALIASES = {"HomologicalAlgebraPackage": "Complexes"}


class HeaderError(ValueError):
    pass


def header_options(source):
    """Yield top-level comma-separated arguments to the first newPackage call."""
    tokens = [match.group() for match in TOKEN.finditer(source)
              if not match.group().startswith("--")]
    try:
        start = tokens.index("newPackage")
    except ValueError as error:
        raise HeaderError("missing newPackage declaration") from error
    if tokens[start + 1:start + 2] != ["("]:
        raise HeaderError("unsupported newPackage declaration")
    stack = [")"]
    argument = []
    for token in tokens[start + 2:]:
        if token in OPEN:
            stack.append(OPEN[token])
        elif token in (")", "}", "]"):
            if not stack or token != stack.pop():
                raise HeaderError("unbalanced newPackage declaration")
            if not stack:
                if argument:
                    yield argument
                return
        if token == "," and len(stack) == 1:
            if argument:
                yield argument
            argument = []
        else:
            argument.append(token)
    raise HeaderError("unterminated newPackage declaration")


def literal_package_list(tokens):
    if len(tokens) < 2 or tokens[0] != "{" or tokens[-1] != "}":
        raise HeaderError("expected a literal list of package names")
    names = []
    expect_name = True
    for token in tokens[1:-1]:
        if expect_name:
            if token in PACKAGE_ALIASES:
                name = PACKAGE_ALIASES[token]
            elif token.startswith('"') and token.endswith('"'):
                name = token[1:-1]
            else:
                raise HeaderError("expected a quoted package name")
            if not PACKAGE_NAME.fullmatch(name):
                raise HeaderError("invalid package name")
            names.append(name)
        elif token != ",":
            raise HeaderError("expected a comma between package names")
        expect_name = not expect_name
    return names


def read_header(filename, expected_name):
    try:
        source = filename.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise HeaderError(f"could not read package source: {filename}: {error}") from error
    return read_header_text(source, expected_name)


def cyclic_components(graph):
    return sorted(
        sorted(component) for component in nx.strongly_connected_components(graph)
        if len(component) > 1 or any(graph.has_edge(node, node) for node in component)
    )


def self_test():
    for edges, expected in (
        ([('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'D')], []),
        ([('A', 'A')], [['A']]),
        ([('A', 'B'), ('B', 'A'), ('C', 'D'), ('D', 'E'), ('E', 'C'), ('F', 'A')],
         [['A', 'B'], ['C', 'D', 'E']]),
        ([('A', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'D'), ('D', 'B')],
         [['A', 'B', 'C', 'D']]),
    ):
        assert cyclic_components(nx.DiGraph(edges)) == expected
    assert cyclic_components(nx.DiGraph()) == []
    assert read_header_text(
        '-- PackageImports => {"Wrong"}\n'
        'newPackage("A", PackageImports => {"B",}, '
        'PackageExports => {HomologicalAlgebraPackage})', 'A'
    ) == [('B', 'PackageImports'), ('Complexes', 'PackageExports')]
    try:
        read_header_text('newPackage("A", PackageImports => otherPackages)', 'A')
    except HeaderError:
        pass
    else:
        raise AssertionError("dynamic dependencies must fail the audit")
    print("PASS: dependency graph and header self-tests")


def read_header_text(source, name):
    """Parse a header fixture using the same option logic as real files."""
    options = list(header_options(source))
    if not options or options[0] != [f'"{name}"']:
        raise HeaderError("package name does not match filename")
    dependencies = []
    seen = set()
    for option in options[1:]:
        if len(option) < 2 or option[0] not in ("PackageImports", "PackageExports"):
            continue
        kind = option[0]
        if option[1] != "=>" or kind in seen:
            raise HeaderError(f"invalid {kind} option")
        seen.add(kind)
        dependencies.extend((dependency, kind)
                            for dependency in literal_package_list(option[2:]))
    return dependencies


def audit(directory, roots):
    graph = nx.DiGraph()
    graph.add_nodes_from(("Core", "User"))
    edge_kinds = defaultdict(set)
    problems = []
    seen = set()
    header_count = 0

    def visit(name):
        nonlocal header_count
        if name in seen:
            return
        seen.add(name)
        graph.add_node(name)
        if name in ("Core", "User"):
            return
        filename = directory / f"{name}.m2"
        if not filename.is_file():
            problems.append(f"missing package source: {filename}")
            return
        try:
            dependencies = read_header(filename, name)
        except HeaderError as error:
            problems.append(f"could not read package header: {filename}: {error}")
            return
        header_count += 1
        for dependency, kind in dependencies:
            graph.add_edge(name, dependency)
            edge_kinds[name, dependency].add(kind)
        for dependency in sorted(set(graph.successors(name))):
            visit(dependency)

    for name in roots:
        visit(name)
    return graph, edge_kinds, problems, header_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=DEFAULT_PACKAGES)
    parser.add_argument("packages", nargs="*")
    parser.add_argument("--edges", action="store_true", help="show every declared edge")
    parser.add_argument("--self-test", action="store_true", help="test the checker")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    directory = args.directory.resolve()
    try:
        roots = args.packages or [line.strip() for line in
                                  (directory / "=distributed-packages").read_text().splitlines()
                                  if PACKAGE_NAME.fullmatch(line.strip())]
    except OSError as error:
        print(f"Dependency audit failed: {error}", file=sys.stderr)
        return 2
    for name in roots:
        if not PACKAGE_NAME.fullmatch(name):
            parser.error(f"invalid package name: {name}")
    roots = sorted(set(roots))
    graph, edge_kinds, problems, header_count = audit(directory, roots)
    print(f"Read {header_count} package headers from {directory}/")
    print(f"Roots: {len(roots)}; dependency edges: {len(edge_kinds)}")
    if args.edges:
        for source, target in sorted(edge_kinds):
            print(f"{source} -> {target} [{', '.join(sorted(edge_kinds[source, target]))}]")
    cycles = cyclic_components(graph)
    print(f"Cyclic components: {len(cycles)}")
    for component in cycles:
        print("  {" + ", ".join(component) + "}")
        for source in component:
            for target in sorted(set(graph.successors(source)) & set(component)):
                print(f"    {source} -> {target} "
                      f"[{', '.join(sorted(edge_kinds[source, target]))}]")
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f"Dependency audit incomplete: {len(problems)} header error(s)",
              file=sys.stderr)
        return 2
    return 1 if cycles else 0


if __name__ == "__main__":
    sys.exit(main())
