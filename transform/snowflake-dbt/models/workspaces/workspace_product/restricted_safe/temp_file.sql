/*
This is a temporary file that is being used to test the introduction of a new schema before
we transfer existing files to the new schema. We need to set up the new schema before we can
fully test that the permissions are set correctly. I do not want to risk the permissions 
being incorrect, and business partners not being able to query data as a result.
We can use this file to confirm the permissions are correct, then migrate the files over.

Relates to https://gitlab.com/gitlab-data/analytics/-/merge_requests/10710
*/

SELECT
  1 AS test_field