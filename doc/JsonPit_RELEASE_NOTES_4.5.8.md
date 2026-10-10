# JsonPit RELEASE NOTES 4.5.8

- Release version: `4.5.8`
- Coordination tag: `v4.5.8`

## Highlights
- Relaxes strict ID assertion in `PitItem.ExtendWith` to allow updates when the incoming payload specifies the matching `Id`.
- Preserves envelope protection against overwriting protected metadata (`Created`, `Modified`, `Deleted`).

## Coordinated Dependencies
- Aligned with RAIkeep synchronized `4.5.8` line.
