---
marp: true
paginate: true
---

# GCS Public Bucket & Object Scanner CLI Tool

---

## Problems
- It's not recommended to use public bucket in GCS (CIS GCP 5.1)
- Public objects not a best practice, only used in some ocassion
- Unexpected use of public buckets / public objects will introduce security concerns

## Solution
- Engineering built the tools to scan the public buckets and public
- Provide report summary to be consumed by involved entities to have transparency about the current GCS state.

## Goals
- The expectation is to ease the team to secure the GCP environment

---
## Overview
- A CLI tool that provide the below features
    - Detects GCS buckets that are publicly accessible.
    - Identifies objects in a GCS bucket that are publicly visible.
    - Email reporting of both
- The tools are lightweight and expandable
