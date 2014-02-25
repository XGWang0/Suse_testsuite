HOW
---
  1. sq-perf-all is the core. ./sq-perf-all SLE12x
  2. testset_performance-run calls sq-perf-all. but TARGET_RELEASE= should be complete before used.
  3. sqperf.service is created when packaging.
  4. NOTE some scripts are done in qa_testset_performance.spec.

TODO
----
  * multilist.
  * sub-commands for manual work.


FIXME
-----
  * the reboot function has issues.