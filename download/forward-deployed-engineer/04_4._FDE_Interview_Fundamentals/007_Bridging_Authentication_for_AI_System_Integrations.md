# Bridging_Authentication_for_AI_System_Integrations

Source: https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems

---

[Home](https://www.educative.io/)

[Courses](https://www.educative.io/search?tab=courses)

[Forward Deployed Engineer for AI Systems](https://www.educative.io/courses/forward-deployed-engineer)

# Bridging Authentication Across Systems

Explore how to connect systems that use different authentication schemes, from delegated user access to workload credentials. Learn how to decide whose authority each connection carries and how tokens are scoped, renewed, rotated, and revoked. Understand how to enforce access per user, field, and tenant even when data is cached or copied.

We'll cover the following...

- [Why Rill’s API rejects a signed-in user](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Why-Rills-API-rejects-a-signed-in-user)
- [Connections that act for a person and connections that act for Rill](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Connections-that-act-for-a-person-and-connections-that-act-for-Rill)
- [When a case token is usable and how it is renewed](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#When-a-case-token-is-usable-and-how-it-is-renewed)
- [Which OAuth controls protect against which attacks](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Which-OAuth-controls-protect-against-which-attacks)
- [Reaching warranty W42 for u17 without sharing signing secrets](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Reaching-warranty-W42-for-u17-without-sharing-signing-secrets)
- [Why the importer can read C99 while u17 cannot](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Why-the-importer-can-read-C99-while-u17-cannot)
- [Rotating v1 and recovering from revocation](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Rotating-v1-and-recovering-from-revocation)

A staff member signs in successfully to Rill Parts’ portal, opens a case, and receives an API access-denied response. Successful login established a portal identity; the case API still needs an authorized caller and a credential it accepts. Bridging authentication means specifying that access contract for each connection while keeping a user’s permissions intact across adapters and copied data.

## Why Rill’s API rejects a signed-in user[#](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Why-Rills-API-rejects-a-signed-in-user)

Suppose Rill’s portal uses SAML single sign-on and SCIM provisioning. Its case API supports delegated and application OAuth access, its warranty API requires OAuth 1.0a, and its supplier API requires an API key plus a client certificate.

Distinguish four concepts:

- **Authentication:** Establishes an identity by answering “Who signed in?”
- **Federation:** Establishes trust in another identity provider’s assertions by answering “Whose identity evidence does the portal accept?”
- **Provisioning:** Creates, updates, or disables accounts and group memberships, answering “Does this account exist and remain active?”
- **Authorization:** Decides which resources and actions an identity may access, answering “May this caller read this case?”

SAML commonly supports federated login. OIDC adds an identity layer to OAuth 2.0; OAuth governs access to protected resources; SCIM supports provisioning. None alone guarantees downstream business permissions.

Rill’s SAML login creates a portal session, not a case-API access token. SCIM group membership supplies policy input; the API still enforces its authorization model. Identify both the human caller and the integration identity used at each downstream boundary.

## Connections that act for a person and connections that act for Rill[#](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Connections-that-act-for-a-person-and-connections-that-act-for-Rill)

**Delegated access** acts with a user’s authorization. **Workload access** acts as an application or service identity. A service account is an identity, not a universal credential format or an OAuth grant.

Under Rill’s assumed provider capabilities, choose this compact connection inventory:

- **Case viewer:** The signed-in user authorizes user-scoped access to the case API through authorization code with PKCE. Request `cases.read`; apply the provider’s user-level restrictions.
- **Nightly importer:** A dedicated application identity uses supported client credentials for the case API’s application permission `cases.read`. It may ingest tenant cases but cannot write them.
- **Warranty adapter:** A tenant-specific, read-only integration identity uses the warranty provider’s OAuth 1.0a request-signing protocol and credential set.
- **Supplier connector:** Its own read-only integration identity presents the supplier API key and an mTLS client certificate, proving possession of the corresponding private key.

Certificate authentication still needs business authorization. OAuth 1.0a signing, API-key presentation, and certificate authentication are distinct mechanisms with separate adapters.

For interactive delegation, authorization code with PKCE is the design default when supported. A **public client**, such as browser-delivered code, cannot securely retain a shared client secret; a **confidential client** can protect credentials in its execution environment. Rill can place delegated token handling in a confidential portal backend.

Rill’s SAML identity provider may authenticate the user during the case provider’s authorization journey. The case provider must still issue its supported API authorization. If application permissions are unavailable, choose provider-supported, administrator-approved delegation with its lifecycle obligations, or renegotiate the unattended workflow. Borrowing a browser session supplies neither a supported workload identity nor a reliable authorization lifecycle.

Classify the proposed connections before deciding where credentials belong.

Match Rill's access contracts

Rill connection

Portal login: staff sign in to Rill

Supplier reader: retrieve supplier data

Nightly importer: ingest tenant cases without a signed-in user

User-scoped case viewer: read cases for the signed-in user

Warranty reader: read warranties for one tenant

Identity and credential arrangement

Dedicated application: client credentials with case API application permission cases.read

Own read-only integration identity: supplier API key plus mTLS client certificate

User delegation: authorization code with PKCE; case API cases.read with user restrictions

Tenant-specific read-only integration identity: OAuth 1.0a signing credentials

Staff identity: SAML federated login; SCIM provisions portal accounts and groups

Connect each Rill connection to its supported arrangement. Use feedback to revise mismatches: portal login is not API authorization, and a service account is not a grant.

Do you find this helpful?

The inventory also identifies separate revocation targets. Disabling a portal account and revoking a connector’s downstream credentials are different operations; the access contract must account for both.

## When a case token is usable and how it is renewed[#](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#When-a-case-token-is-usable-and-how-it-is-renewed)

Rill’s case API expects audience `case-api`. Assume these issuance rules:

- **Viewer:** An access token with scope `cases.read` lasts 15 minutes. A refresh token is issued only after the required offline-access consent and policy approval.
- **Importer:** An application access token also lasts 15 minutes. No refresh token is issued; the importer obtains another access token using its workload credentials.

An ID token establishes identity for its intended client; it cannot substitute for an API access token. Match issuer, audience, tenant, subject or application identity, expiry, and permissions to the receiving API’s validation contract. Use provider libraries or supported introspection; tokens need not be JWTs, and decoding a JWT alone does not validate it.

Isolate token caches by tenant, client, identity, resource, and permission set. Store refresh tokens and workload credentials in protected backend storage, track expiry, and renew through the supported grant.

If renewal fails because delegated consent was revoked, mark the connection `reconnect-required` and route recovery to Rill’s client identity administrator. Never substitute the importer’s broader token to keep the viewer working.

## Which OAuth controls protect against which attacks[#](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Which-OAuth-controls-protect-against-which-attacks)

RFC 9700, the OAuth 2.0 Security Best Current Practice published in January 2025, is this lesson’s security baseline.

Its requirements depend on client type and threat:

- **Redirect substitution:** Authorization servers must compare redirect URIs using exact string matching. The only exception is the port number in localhost redirect URIs for native apps.
- **Authorization-code interception or injection:** Public clients must use PKCE, and confidential clients should use it. Authorization servers must support PKCE.
- **Browser transaction attacks:** Clients must prevent cross-site request forgery (CSRF). PKCE provides that protection only when the client has confirmed that the authorization server supports it; otherwise, use a one-time state value.

PKCE mitigates authorization-code interception: an attacker who intercepts a code cannot exchange it for an access token without the matching code verifier.

RFC 9700 also states that the resource owner password credentials grant must not be used and that clients should not use the implicit grant or other response types that issue access tokens from the authorization endpoint. Refresh tokens issued to public clients must be sender-constrained or rotated.

PKCE does not protect an access token after issuance. To limit replay of stolen tokens, RFC 9700 recommends sender-constrained access tokens, such as mutual TLS or DPoP, along with audience and privilege restrictions.

For native apps specifically, RFC 8252 requires authorization through an external user-agent and requires public native apps to implement PKCE. Those native-app requirements should not be generalized to every OAuth client.

## Reaching warranty W42 for u17 without sharing signing secrets[#](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Reaching-warranty-W42-for-u17-without-sharing-signing-secrets)

A tempting broker design accepts any logged-in user, trusts a request parameter `tenant_id`, chooses that tenant’s connector, and returns the full downstream object. A caller can substitute tenant T2 or request an unrelated warranty while the broker supplies privileged credentials. This is a **confused-deputy failure**: A privileged component exercises its authority for a caller who lacks the corresponding permission.

For Rill, assume current policy permits user `u17` in tenant `T1` to read assigned case `C42`, and C42 references warranty `W42`. Trace the authorized route:

1. The backend validates the portal session and derives `u17` and `T1` from trusted identity context. A request parameter cannot select T2’s authority.
2. It checks current policy for u17’s relationship to C42, the requested read action, and C42’s verified link to W42. An arbitrary warranty identifier is insufficient.
3. It maps trusted T1 to T1’s approved warranty connector and requests the bounded operation “read W42.” The caller cannot choose an arbitrary destination URL or operation.
4. Only the adapter retrieves T1’s OAuth 1.0a credential set from protected storage and signs the request using a supported library.
5. The backend returns only fields u17 may receive. Signing secrets and general-purpose privileged tokens never enter the response.

The supplier adapter similarly presents its key and certificate at its own outbound boundary. A controlled credential broker authenticates and authorizes callers, selects approved downstream identities, and mediates bounded operations, or it performs an explicitly supported token exchange. It cannot universally convert SAML assertions into arbitrary API keys, OAuth tokens, or legacy credentials.

## Why the importer can read C99 while u17 cannot[#](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Why-the-importer-can-read-C99-while-u17-cannot)

The importer copies T1 cases `C42` and `C99`, including `internal_cost`. Current application policy permits u17 to read only C42, excludes `internal_cost`, and grants no write action.

A connector’s broad access must never become the application user’s effective permission. Preserve tenant and source identifiers with each copied record, and retain or resolve the policy information required for enforcement.

For a cached C42 read:

1. Derive T1 from the trusted session and constrain retrieval to T1. Check object and row authorization before returning data; C99 fails even within T1.
2. Consult the current policy service on every read. This is Rill’s permission-freshness contract: A policy-service failure denies access, and a reassignment takes effect on the next read.
3. Project only permitted fields, removing `internal_cost` from C42. Apply the same restriction to cached responses, search results, and retrieval used by an AI feature.
4. Recheck the requested action before every downstream tool call. Permission to read C42 grants no case-write authority.

Successful connector authentication can therefore coexist with a denied user request. Test the actual response boundary, including what happens after an assignment changes.

Test Rill’s access boundaries

1.

Unless stated otherwise, u17 has a trusted T1 session, is assigned C42, and current policy is available. u17 requests only permitted fields from cached C42. Allow or deny?

A.

Deny

B.

Allow

---

1 / 9

Cached business data cannot authorize its own disclosure. Filtering only at ingestion would fail here because the shared copy intentionally contains records and fields for callers with different permissions.

## Rotating v1 and recovering from revocation[#](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Rotating-v1-and-recovering-from-revocation)

Use least-privilege integration identities isolated by client and environment. Protect secrets and private keys, restrict retrieval to the relevant adapter, and name two owners: The client identity administrator owns consent and reauthorization; the integration operator owns connector rollout.

For planned supplier rotation:

1. Register the replacement key and certificate as version v2 within the provider-supported overlap.
2. Store v2 securely and test an authorized read using it.
3. Move connector instances to v2 and verify that no instance still uses v1.
4. Retire v1 before the overlap ends. Monitor certificate expiry early enough to complete renewal.

If overlap is unavailable, arrange an explicit cutover with a planned pause rather than promise zero downtime. Track access tokens issued under old OAuth client credentials separately: Replacing a stored secret does not necessarily invalidate already-issued tokens.

For compromise, revoke promptly instead of retaining planned overlap, invalidate local credential and token caches, and follow supported token-revocation and incident procedures. When delegated consent is revoked, mark the connection `reconnect-required` and route recovery to the named administrator.

Now specify a separate access contract for Vale Service’s report viewer and background archive. Staff use OIDC login and SCIM provisioning. The report API offers delegated authorization code with PKCE but no application permissions.

Try writing the contract from a blank page first. Then audit the proposal below and revise the design, resolving:

- Whether the archive can run after sign-out.
- How the attachment adapter stays bounded.
- How revocation and rotation change operation.

Vale Service: Access-Contract Review

Your task

You are Vale Service’s integration architect. Consider how you would structure an access-contract memo, then review the proposal below. Staff use OIDC login and SCIM provisioning. The report API supports only delegated authorization code with PKCE, audience `reports-api`, scope `reports.read`, and 10-minute access tokens. Refresh tokens require approved offline access; there are no application permissions. The archive must run after staff sign out. A legacy attachment API accepts a tenant-specific service API key and supports two active keys during rotation. User `u8` belongs to `V1` and may read assigned report `G9`, excluding `margin`; u8 has no write permission. The archive connector may read all V1 reports only if supported delegation is approved. Consent is subsequently revoked. Specify identities, flows, resources, permissions, protected storage, token-cache isolation, renewal, ownership, tenant/row/field/action enforcement, and observable allow/deny tests. Then audit the proposal and revise your contract, including any feasibility constraints.

Tap any claim to classify it, and click on References to verify authorities.

TOVale Service integration teamFROMAccess-contract proposal authorDATEOctober 26, 2026SUBJECTProposed report viewer, background archive, and attachment access

Background

Vale Service needs an interactive report viewer, an archive that continues after staff sign out, and a legacy attachment adapter. The report provider offers delegated authorization code with PKCE but no application permissions. Attachment credentials are tenant-specific, and the attachment provider permits two active keys during rotation.

Issue

Review questions: Which identities and grants can actually support each connection? What may u8 receive from live and archived data? What prevents the attachment adapter from exercising another tenant’s authority? What changes after consent revocation, and who owns recovery and key rollout? Revise the contract and give observable tests for each boundary.

Analysis

The report provider supports an archive-only application permission, `reports.read`, through client credentials. Register a service identity and use that grant for all-V1 ingestion; no delegated authorization or offline-access approval is needed.

OIDC login and SCIM provisioning establish downstream report authority, so the viewer may send its OIDC ID token to `reports-api`. As an archive fallback, reuse the staff member’s browser session after sign-out; the lesson’s distinction between login and provisioning makes that session sufficient authorization.

Once staff are signed in, trust their supplied `tenant_id` to select the attachment key and return complete archived reports, including `margin`, because the archive connector could read them. Retry revoked consent indefinitely. During attachment rotation, retire the old key first and then roll out the replacement.

Keep refresh tokens and attachment keys in protected backend storage accessible only to the relevant components; do not expose them in browser responses, URLs, or logs. Isolate token caches by tenant, client, identity, resource, and permission set. Track the 10-minute access-token expiry and renew only through the supported grant. Preserve tenant and source identifiers on archived records, consult current policy on every read, deny on policy-service failure, project permitted fields, and recheck actions before downstream calls.

Conclusion

The final contract must explicitly decide whether the post-sign-out archive is feasible under the supplied provider capabilities. An unmet approval or delegation dependency must remain a deployment constraint, not an assumed capability.

Recommendation

Attach observable tests to the revised memo: u8 receives only permitted G9 fields from live and archived reads; other V1 reports, other tenants, margin, and writes are denied. Test tenant-parameter tampering, an unrelated attachment, assignment removal, policy-service failure, wrong-audience tokens, and ID-token substitution. Test approved archive operation after sign-out, expiry renewal, revoked-consent recovery, and replacement-key rollout while the old key remains active.

Do you find this helpful?

A contract can correctly conclude that a requested workflow is not yet feasible. Naming an archive identity cannot create application permissions the provider lacks. That feasibility decision also separates failures requiring administrator reauthorization from transient failures that ordinary retries might resolve.

Bridging authentication is rarely about choosing a single protocol. It is about deciding, for every connection, whose authority it carries, how its credentials are stored and renewed, and what happens when they expire or are revoked. With those decisions made explicit, the next lesson turns to what happens when calls fail, hit rate limits, or succeed silently with the wrong result.

Choosing How Data Moves Between Systems

Handling Failures, Rate Limits, and Silent Errors

Ask

[Why Rill’s API rejects a signed-in user](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Why-Rills-API-rejects-a-signed-in-user)

[Connections that act for a person and connections that act for Rill](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Connections-that-act-for-a-person-and-connections-that-act-for-Rill)

[When a case token is usable and how it is renewed](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#When-a-case-token-is-usable-and-how-it-is-renewed)

[Which OAuth controls protect against which attacks](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Which-OAuth-controls-protect-against-which-attacks)

[Reaching warranty W42 for u17 without sharing signing secrets](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Reaching-warranty-W42-for-u17-without-sharing-signing-secrets)

[Why the importer can read C99 while u17 cannot](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Why-the-importer-can-read-C99-while-u17-cannot)

[Rotating v1 and recovering from revocation](https://www.educative.io/courses/forward-deployed-engineer/bridging-authentication-across-systems#Rotating-v1-and-recovering-from-revocation)