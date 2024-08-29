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
  * it's been hard to get reviews from people - note that you can filter PRs by "awaiting review by you". 
  * what should you do when you review? find obvious issues, note clear improvements to be made, test it locally even if checks pass... "light version of JSAG review"
  * **action item** (Doug/Mahrud): wiki page with summary of what reviewers should do
  * similarly, you can see issues you've been assigned (we have many open issues!)
- Onboarding new people: there's a new overview of M2 repositories on the github home page, but no real info on how to join (e.g., how to join organization on GitHub, how to join Zulip, etc.)
  * **action item**: add info on how to join.
- Complexes PR
  * want to make it preloaded, merge old chain complexes code and tests into complexes, and make it work with all other packages
  * first PR is just to get M2 ready to do all this 
  * after this, many (easy) compatibility changes to packages - package maintainers will be assigned as reviewers
  * a few packages (TateOnProducts and SpectralSequences) require more serious changes
  * currently, tests are failing because change to nullhomotopy is incompatible with AInfinity package
  * goal is to have it ready well before November release
