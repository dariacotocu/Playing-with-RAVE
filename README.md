# Playing with RAVE

Live performance system combining guitar with two RAVE models. The guitar dynamics drive the balance between an orchestral model (Sol Ordinario) and a percussion model. Every 20 seconds both models jump to a random point in their latent space.

Presented as a demo at the NIME 2026 workshop *"What Makes it Fun? Mapping Playful Interaction in Music-Making with AI"*.

## How it works

Guitar amplitude is analysed in real-time and mapped across 3 states:

- **Quiet** — Sol Ordinario only
- **Mid** — both models mixed
- **Loud** — percussion dominates

Every 20 seconds both models jump to a new random point in their latent space, introducing unpredictability for both performer and audience.

## Setup
