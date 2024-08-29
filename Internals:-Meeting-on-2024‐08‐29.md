#### Topics Discussed:
- M2 future events 
  * **action item**: add upcoming "Under the Hood" seminars to Events tab on website
- Meta discussion
  * creating agendas (or a rolling list of issues) + ensuring notes are taken (or at least a record of what is discussed)
  * frequency: monthly, with possible additional meeting times for international contributors
  * what should be discussed in M2 internals?
  * occasional overview of internals for new attendees? 
- PR requests
  * example of PR review (NB: "add single comment" functionality, ability to break down PR review into individual commits)
  * anyone in the M2 organization can now be asked to review PRs (only maintainers can formally request a review; others should feel free to tag relevant people)
  * it's been hard to get reviews from people - note that you can filter PRs by "awaiting review by you". (Similarly, you can see issues you've been assigned - we have many open issues!) 
  * what should you do when you review? find obvious issues, note clear improvements to be made, test it locally even if checks pass... "light version of JSAG review"
  * **action item** (Doug/Mahrud): wiki page with summary of what reviewers should do

- Onboarding new people
  * there's a new overview of M2 repositories on the github home page, but no real info on how to join (e.g., how to join organization on GitHub, how to join Zulip, etc.)
  * **action item**: add info on how to join.
- Complexes PR
  * goal: have it be preloaded, merge old chain complexes code and tests into complexes, and make it work with all other packages
  * first PR is just to get M2 ready to do all this 
  * after this, many (easy) compatibility changes to packages - package maintainers will be assigned as reviewers
  * a few packages (TateOnProducts and SpectralSequences) require more serious changes
  * goal is to have it ready well before November release
  * idea: "LegacyChainComplexes" package for short-term compatibility
- Profiling M2 code
  * a tool for understanding which exact lines in M2 were run, what percent of time it took, etc., when an M2 command is run
  * currently a draft PR (and not yet documented)
  * goal: use this to methodically go over core and highlight things that slow it down
  * how to find participants in this proces? google form circulated to google group? (workshop might not be ideal forum) 
  
- Recent pull requests
  * pseudocode: gives a more readable form of "disassemble"
  * changes in error location and descriptions, 
  * access to previous M2 session history 
  * M2 emacs: deferred for later
