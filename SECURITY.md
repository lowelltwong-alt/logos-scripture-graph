# Security Policy

## Reporting a vulnerability

Please report suspected vulnerabilities privately through GitHub's security-advisory
workflow for this repository. Do not open a public issue containing exploit details,
credentials, private source material, or personal data.

Include the affected revision, a minimal reproduction, likely impact, and any safe
mitigation you have identified. The maintainer will acknowledge the report, assess
scope, and coordinate disclosure after a fix or documented disposition exists.

## Supported surface

The default branch and the latest tagged release, when one exists, are the supported
public surfaces. Scratch branches, candidate data, multi-model research lanes, draft
pull requests, and unreviewed MCP experiments are evidence under review, not supported
releases.

## Security boundaries

- Never commit secrets, access tokens, private conversations, or licensed source
  payloads that are not cleared for redistribution.
- MCP access described by this repository is local, stdio, and read-only. Remote MCP
  and repository-write tools are disabled unless a later reviewed release says
  otherwise.
- Scripture, chunk, graph, retrieval, and theological claims remain governed by their
  provenance and trust-zone contracts. Tool output is not authority.
- Security reports do not authorize changes to canonical Scripture data, project
  governance, or theological policy.
