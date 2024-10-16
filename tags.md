# Tags on RFCs

We categorize RFCs with tags to enrich searches. The meaning of tags is given below.

### `protocol`
Defines one or more [protocols](concepts/0003-protocols/README.md) that explain how messages are passed to accomplish a stateful interaction.

### `decorator`
Defines one or more [decorators](concepts/0011-decorators/README.md) that act as mixins to [DIDComm](concepts/0005-didcomm/README.md) messages. Decorators can be added to many different message types without explicitly declaring them in message schemas.

### `feature`
Defines a specific, concrete feature that [agents](concepts/0004-agents/README.md) might support.

### `concept`
Defines a general aspect of the Aries mental model, or a pattern that manifests in many different features.

### `community-update`
An RFC that tracks a community-coordinated update, as described in [RFC 0345](concepts/0345-community-coordinated-update/README.md). Such updates
enable independently deployed, interoperable agents to remain interoperable
throughout the transition.

### `credentials`
Relates to [verifiable credentials](https://www.w3.org/TR/vc-data-model/).

### `rich-schemas`
Relates to next-generation schemas, such as those used by [https://schema.org](https://schema.org), as used in verifiable credentials.

### `test-anomaly`
Violates some aspect of our [policy on writing tests for protocols before allowing their status to progress beyond DEMONSTRATED](/README.md#accepted). RFCs should only carry this tag temporarily, to grandfather something where test improvements are happening in the background. When this tag is applied to an RFC, unit tests run by our CI/CD pipeline will emit a warning rather than an error about missing tests, IFF each implementation that lacks tests formats its notes about test results like this:

```markdown
name of impl | [MISSING test results](/tags.md#test-anomaly)
```