# Noepedia Pilot: AISocket + OpenPCB Commons

> **Purpose:** use AISocket as the first live producer of structured physical traces, and OpenPCB Commons as the first domain in which Noepedia must work as a real storage and search system rather than only as a philosophical architecture.

This pilot is deliberately practical.

It should force Noepedia to prove that it can receive evidence from real devices, preserve incomplete knowledge without pretending it is finished, retrieve useful relational cuts later, and support a domain whose objects are heterogeneous: boards, components, images, measurements, nets, repair cases, instruments, traces, hypotheses, and reusable parts.

---

## 1. Roles of the three projects

### AISocket — contact with the world

AISocket provides bounded observation, experiment, action, and trace production.

It should be able to say:

~~~text
which body produced the trace
which passport/version was active
which firmware/configuration was active
which tool was invoked
under which mandate
what was observed before
what action or measurement was performed
what was observed after
which limits / calibration / units applied
~~~

AISocket does not decide that the trace is settled knowledge.

It returns evidence.

### OpenPCB Commons — first real knowledge domain

OpenPCB Commons provides a concrete, difficult, naturally incomplete field:

~~~text
boards
components
markings
pads
nets
images
geometry
measurements
instruments
schematic fragments
functional blocks
failures
repairs
second-life uses
unknowns
disagreements
~~~

OpenPCB is therefore not only a demonstration dataset.

It is a domain that can expose whether Noepedia's object identity, provenance, relation networks, staging, search, revision, and retrieval actually work.

### Noepedia — persistent field, storage, and search

Noepedia is the persistent addressable semiotic field.

For this pilot it must do two jobs at once:

1. **store** structured OpenPCB / AISocket material and its provenance;
2. **retrieve** useful objects and relation-network cuts for later humans, LLMs, tools, and experiments.

All persistent field operations remain mediated by the Socratic Daimonion.

---

## 2. Minimal technical requirements for the pilot

The first implementation does not need the final universal architecture.

It must support enough structure to run a complete loop.

### 2.1 Stable addressable identity

Every persistent object needs a stable ID independent of its human-readable label.

Examples:

~~~text
BOARD
COMPONENT
PAD
NET
IMAGE
GEOMETRY
MEASUREMENT
INSTRUMENT
EXPERIMENT
TRACE
REPAIR_CASE
FAILURE_MODE
SECOND_LIFE_USE
SOURCE
RAW_BLOB
RELATION
NETWORK
RULE
REVISION
~~~

A label such as a component marking, product name, or board code is a searchable projection onto that identity, not the identity itself.

### 2.2 Triplet relation networks

The pilot must support domain predicates such as the following. These do not change the storage grammar; every relation remains an ordinary SPO triplet:

~~~text
BOARD ── HAS_COMPONENT ──> COMPONENT
COMPONENT ── MARKED_AS ──> LABEL
PAD ── CONNECTED_TO ──> NET
MEASUREMENT ── OBSERVED_ON ──> PAD
MEASUREMENT ── PRODUCED_BY ──> INSTRUMENT
TRACE ── ABOUT ──> BOARD
REPAIR_CASE ── REPLACED ──> COMPONENT
PART ── REUSED_IN ──> SECOND_LIFE_USE
CLAIM ── SUPPORTED_BY ──> EVIDENCE
~~~

Networks and relation types must themselves remain addressable and revisable.

### 2.3 Provenance as first-class structure

Every important observation or inferred relation must be able to point back to:

~~~text
source
contributor / initiating process
instrument
calibration
method
timestamp
body / passport version
firmware or configuration version
raw trace
conditions
uncertainty
revision history
~~~

The pilot fails if a useful-looking relation cannot later answer:

> **How did we come to believe this?**

### 2.4 Raw data / blob support

OpenPCB produces payloads whose **bytes** should not be exploded into triplets:

~~~text
photographs
microscope images
waveforms
binary captures
3D geometry
board scans
datasheets
logs
firmware dumps where legally shareable
~~~

The image, waveform, geometry file, or other artifact still appears in Noepedia as an ordinary addressable object connected by SPO relations. Its large byte payload may live outside the triplet matrix. A RAW_BLOB role therefore needs at least:

~~~text
stable object ID
content hash
MIME / media type
size
storage location or blob payload
source
timestamp
permissions
relations to the objects it documents
~~~

The first implementation may use a separate content-addressed file/object store behind the field if storing large bytes directly in the graph is impractical.

What matters is that the blob remains addressable through Noepedia and cannot lose its provenance.

### 2.5 Staging / inbox

AISocket traces, human notes, model hypotheses, and imported files must be accepted before their final place is known.

The pilot therefore needs:

~~~text
INBOX / STAGING
→ identify
→ compare
→ clarify
→ link
→ promote / remain unresolved / reject promotion
~~~

Submission authority and trusted-write authority are different permissions.

### 2.6 Search

OpenPCB is the first place where Noepedia must prove that it is not merely an archive.

At minimum search should support:

- labels and part markings;
- exact object IDs;
- object type;
- relations and relation paths;
- provenance / source;
- board family;
- component occurrence across boards;
- failure / repair relations;
- instrument and measurement type;
- unknown / disputed / provisional status;
- second-life compatibility relations.

Useful queries should include questions such as:

~~~text
Where else does this marked component appear?

Which boards contain this connector family?

Show measurements supporting this reconstructed net.

Which repair cases involved this failure pattern?

Which salvaged motors have a compatible voltage / encoder / mounting relation?

What evidence contradicts this schematic fragment?

Which knowledge came from this instrument version?

What is still OPEN on this board?
~~~

Text search alone is not enough.

### 2.7 Semiotic-cut retrieval

A query should be able to return more than a list of filenames or sentences.

The Daimonion should be able to reconstruct a task-relevant cut containing:

~~~text
objects
relations
network rules
context
provenance
evidence / counterevidence
uncertainty
coverage
raw-artifact references
revision history
permissions
~~~

This is the pilot's concrete test of **epistemic teleportation**.

### 2.8 Revision without erasure

A wrong component identification, net relation, or repair hypothesis must be correctable without destroying the old state.

The pilot requires:

~~~text
old assertion
+ new evidence
+ explicit revision
+ preserved provenance
~~~

A changed map must preserve why it changed.

### 2.9 Permissions and audit

The Daimonion must mediate persistent operations.

The pilot needs at least:

~~~text
read permission
submit permission
promote / trusted-write permission
revise permission
restricted-object permission
transaction log
~~~

A visitor may be allowed to contribute a trace without being allowed to rewrite a settled relation.

### 2.10 Export, backup, and portability

The pilot must not make knowledge hostage to one server implementation.

At minimum, persistent objects, triplets, provenance, revisions, and blob references need an exportable representation.

---

## 3. AISocket trace envelope required by Noepedia

For the pilot, AISocket should be able to emit a minimally normalized trace envelope.

Conceptually:

~~~text
TRACE_ID
TIME
BODY_ID
PASSPORT_VERSION
FIRMWARE_OR_CONFIG_VERSION
MANDATE / ACTOR
TOOL_ID
TARGET_OBJECT(S)
PRE_STATE
ACTION_OR_MEASUREMENT
PARAMETERS
UNITS
CALIBRATION_REF
POST_STATE / RESULT
ERROR / ALARM
RAW_ARTIFACT_REFS
LOCAL_SAFETY_DECISION
~~~

Not every device will populate every field.

The important requirement is that absent fields remain absent or explicit UNKNOWN, rather than being silently invented later.

---

## 4. OpenPCB data model for the first pilot

The first OpenPCB board does not need a complete universal PCB ontology.

A useful minimum is:

~~~text
BOARD
 ├─ images
 ├─ geometry
 ├─ components
 │   ├─ markings
 │   ├─ package
 │   └─ candidate identity
 ├─ pads
 ├─ nets
 ├─ measurements
 ├─ schematic fragments
 ├─ functional blocks
 ├─ failures
 ├─ repairs
 ├─ reusable parts
 └─ OPEN questions
~~~

Each branch should carry provenance where appropriate.

A board may remain mostly unknown and still be a valid Noepedia object.

---

## 5. First end-to-end experiment

A good first experiment is intentionally small.

1. Register one real board as a nameless/stable Noepedia object.
2. Attach two board images as raw artifacts.
3. Add several visible component markings.
4. Connect one AISocket instrument.
5. Perform one safe measurement.
6. Ingest the resulting trace into staging.
7. Let the Daimonion attach the trace to the correct board / pad / component context.
8. Promote one supported relation.
9. Search for that relation later through another label or object path.
10. Revise one intentionally wrong or provisional placement without deleting its history.

The experiment succeeds only if a second participant can retrieve the evidence path without relying on the original chat or operator's memory.

---

## 6. Acceptance tests

The pilot should eventually demonstrate all of the following:

- a board can be stored before it is fully understood;
- an unnamed object can later receive labels without changing identity;
- one AISocket trace can be ingested with full provenance;
- raw data can remain staged without being promoted to knowledge;
- a supported relation can be promoted;
- a wrong relation can be revised non-destructively;
- a query can find one component across several boards;
- a repair/failure pattern can be searched relationally;
- a second-life part can be found through compatibility relations;
- a query can return the evidence behind a claim;
- a query can return what is still unknown;
- unauthorized persistent writes are rejected or downgraded to staging;
- the Daimonion can return a compact task-relevant semiotic cut instead of the whole archive.

---

## 7. What this pilot is meant to teach us

AISocket tests whether Noepedia can remain connected to **new experience**.

OpenPCB tests whether Noepedia can remain useful under **heterogeneous, partial, constantly revised knowledge**.

Together they should reveal what the first real Daimonion, storage layer, indexing strategy, object identity mechanism, provenance model, and retrieval protocol actually need to become.

This is preferable to inventing the final database in isolation.

> **Build the smallest field that can receive a real trace, preserve it honestly, and help the next investigator begin farther ahead.**
