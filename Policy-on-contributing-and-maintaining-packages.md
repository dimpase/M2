Macaulay2 packages are a community effort, written and maintained by the Macaulay2 mathematical community. As such, we ask that all contributors approach this work with collegiality and respect, remembering that you are communicating with other humans. Before opening a Pull Request (PR) on an existing package, we strongly recommend reaching out to the maintainer directly first. This helps avoid duplicated effort, ensures your contribution aligns with the maintainer's vision for the package, and fosters the kind of collaborative spirit that makes the Macaulay2 community thrive.

## 1. Contributing to existing packages

Every Macaulay2 package has a listed maintainer who is the point of contact for all issues related to the package.

**Contributing code:** Anyone wishing to contribute to an existing package should open a Pull Request and tag the maintainer for review. The maintainer must approve all code additions. As a matter of etiquette, we recommend reaching out to the maintainer before opening a Pull Request to align on scope and approach.

**Reporting a bug or requesting a feature:** Open an issue in GitHub and tag the active maintainer. The maintainer is responsible for acknowledging the issue and coordinating a response (see [Section 3](#3-orphaned-and-adopted-packages)).

**Contributing to orphaned packages:** Packages without an active maintainer may still receive Pull Requests. These will be reviewed by the PR Editor.

## 2. Maintaining a package

**Role of the maintainer:** A maintainer is a single person responsible for communication and oversight related to a package. Specifically, a maintainer is expected to:

- Acknowledge bug reports and feature requests within 60 days (this does not mean that a bug needs to be fixed in this timeframe, but it needs to be acknowledged).
- Coordinate with package authors and contributors to address issues.
- Keep the package functional across new Macaulay2 releases.
- Designate a successor if they can no longer fulfill the role.

**Changing a maintainer:** If a maintainer can no longer maintain a package, it is their responsibility to designate a new maintainer — preferably from among the package's authors or contributors — and initiate a pull request with the updated package information.

**Stepping down without a successor:** If a maintainer steps down without designating a replacement, the package will be marked as orphaned (see [Section 3](#3-orphaned-and-adopted-packages)).

## 3. Orphaned and adopted packages

**When a package becomes orphaned:** A package will be tagged as orphaned by the PR Editor in any of the following situations:

- The package has had a critical issue making it unusable for more than two M2 releases or a year (whichever is longer).
- The maintainer has failed to respond to/acknowledge issues or emails within 60 days (in this case, request the orphaned tag).
- The maintainer has removed themselves without designating a successor.

**Requesting the orphaned tag:** If you believe a package should be marked orphaned (e.g., the maintainer has been unresponsive), contact the Issue Editor with documentation of your outreach attempts. The Issue Editor will make the final determination.

**Adopting an orphaned package:** A package can be adopted in the following ways:

- **Volunteer:** Contact the Issue Editor to express interest in maintaining an orphaned package.
- **Recruited:** The Issue Editor may reach out to active contributors to a package and invite them to become maintainer.
- **Contribute and maintain:** Submit a Pull Request that resolves outstanding issues; upon acceptance, you may be offered the maintainer role.