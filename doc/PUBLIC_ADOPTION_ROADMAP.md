# Public adoption and discoverability

Future work agreed on November 19, 2026. The aim is to make RAIkeep easier to find,
evaluate and contribute to, and to earn independent evidence of sustained use.
These items are a backlog, not claims of adoption or a promise of eligibility
for any external program.

## Lead with JsonPit and Umgodi JSON

JsonPit and `umgodi-json` should lead public introductions and examples. They
provide the concrete use case: historical JSON persistence shared across .NET
and Python, with cloud-backed files and CLI tools. Introduce RAIkeep as the
supporting umbrella and Inqaba as the Python foundation when those details help
users adopt the storage packages.

Start with a paired .NET/Python quickstart, explain when this storage model fits
and where its tradeoffs matter, and demonstrate recovery/history with disposable
data. Validate interoperability and limitations against the released packages.
Build case studies around real use of these two packages before promoting the
entire suite as a single offering.

## Supporting work

- **Package discovery:** use consistent RAIkeep metadata across all 11 NuGet
  packages and three PyPI distributions. In particular, add the umbrella tag to
  OsLibCore, JsonPit, RaiImage and PitSeeder. Keep the component inventory clear
  about active packages and legacy distributions.
- **First successful use:** provide short, reproducible examples for the main
  libraries and CLIs, with expected output, installation requirements and links
  from each package page. Validate them against published packages.
- **Real-world references:** document useful deployments and case studies with
  the owners' permission. Identify maintainer-owned examples as such; distinguish
  them from independent adoption. Link external articles or discussions when
  they actually exist.
- **Contributor experience:** explain local setup, tests and review expectations;
  identify suitable first contributions; keep issues and responses useful.
- **Evidence over time:** periodically record public contributors, independent
  integrations, issue participation and package usage with sources and dates.
  Download totals are not unique users. Stars and forks are supporting signals,
  not a substitute for actual use, and must not be purchased or manufactured.

Start with discoverability and one complete example per major use case. Decide
owners and priorities before beginning a broader outreach effort. No outreach
messages or recurring monitoring have been authorized by this roadmap.
