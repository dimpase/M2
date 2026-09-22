-- Experimental out-of-process frontend. It does not replace Core::roots.
-- Set FLINT_ROOTS_BINARY to the absolute path of the compiled roots executable.
flintRoots = method(Options => true);
flintRoots RingElement := {Precision => -1, Unique => false} >> opts -> input -> (
    p := if instance(ring input, FractionField) then numerator input else input;
    (R, mapR) := flattenRing ring p;
    if numgens R > 1 then (
        p = mapR p;
        used := positions(transpose exponents p, e -> any(e, j -> j != 0));
        if #used == 0 then return {};
        if #used != 1 then error "expected a univariate polynomial";
        p = substitute(p, (baseRing R)(monoid[R_(used#0)])));
    R = ring p;
    if numgens R != 1 then error "expected a univariate polynomial";
    if p == 0 then error "expected a nonzero polynomial";
    K := coefficientRing R;
    exact := K === ZZ or K === QQ;
    inputBits := if exact then 53 else precision K;
    bits := if opts.Precision == -1 then inputBits else opts.Precision;
    kind := if exact then "exact" else "mpfr";
    n := first degree p;
    if n == 0 then return {};
    serialize := c -> if exact then toString c
        else replace("p[0-9]+", "", toExternalString c);
    infile := temporaryFileName(); outfile := temporaryFileName(); errfile := temporaryFileName();
    f := openOut infile;
    f << n << " " << bits << " " << kind << " " << inputBits << endl;
    scan(0..n, j -> (
        c := lift(coefficient(R_0^j, p), K);
        f << serialize realPart c << " " << serialize imaginaryPart c << endl));
    close f;
    quotePath := s -> "'" | replace("'", "'\\''", s) | "'";
    binary := getenv "FLINT_ROOTS_BINARY";
    if binary == "" then error "set FLINT_ROOTS_BINARY to the prototype executable";
    status := run("M2_FLINT_ROOTS_TRIALS=1 " | quotePath binary | " flint " | quotePath infile |
        " 1 > " | quotePath outfile | " 2> " | quotePath errfile);
    output := get outfile; errors := get errfile;
    scan({infile, outfile, errfile}, removeFile);
    if status != 0 then error errors;
    parseReal := s -> if s == "0" then 0_(RR_bits)
        else value replace("e", "p" | toString bits | "e", s);
    result := apply(drop(lines output, 1), line -> (
        fields := separate(" ", line);
        (parseReal fields#0) + ii * (parseReal fields#1)));
    -- Deliberately match current rawRoots: Unique is presently ignored there.
    result)
