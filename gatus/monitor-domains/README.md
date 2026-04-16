# Monitor when a domain changes status

e.g. when a .dev domain changes from "pending delete" from something else, which may indicate that the domain is now available for registration.

For example, let's pretent google.dev is currently in "pending delete" status. So you wanna know when it becomes available (or just change status to something else).

- Access: https://rdap.org/domain/google.dev
- Will resolve to the actual API endpoint: https://pubapi.registry.google/rdap/domain/google.dev
    - Different RDAP providers may have different APIs, so it's necessary to hit the first link to find the actual API endpoint.
- Look for the "status" field in the response, which may indicate "pending delete".
    - Different RDAP providers may have different status values. And or completely different JSON content.

From there you just keep monitoring the status field for changes. If you know the values you can be more precise.

[monitor-google.dev-pending-delete.yml](monitor-google.dev-pending-delete.yml) is an example of how to monitor the google.dev domain for changes in its status.