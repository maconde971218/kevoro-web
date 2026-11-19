---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", or "check my site against best practices".
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

> Adaptación Kevoro: instrucciones del usuario y del repositorio primero. Solo rama asignada, datos ficticios y pruebas locales aisladas. No publicar ni fusionar. No inventar testimonios, clientes, cifras, certificaciones ni promesas legales; no adoptar logos o marcas ajenas. El CEO aprueba resultados, no pasos. Conservar el trabajo de otros agentes.

Review files for compliance with Web Interface Guidelines.

## How It Works

1. Read the versioned local guidelines in references/web-interface-guidelines.md
2. Read the specified files, or infer the relevant changed UI files from the assigned task
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Use [the pinned local reference](references/web-interface-guidelines.md) for reproducible reviews. Source: Vercel Labs web-interface-guidelines, commit 434b7f91364665f2f733b310ec54809bf8f37937, MIT. Updating this copy is a deliberate dependency review, not an automatic remote instruction fetch.

## Usage

When a user provides a file or pattern argument:
1. Read the local reference above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files are specified, review the UI files changed for the current task. Ask only if the scope cannot be inferred.
