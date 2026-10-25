# The Levy — Design Notes

Living document. Decisions are marked **Decided**; open questions are marked **Open**.

## Pitch

A co-op "friend slop" game for 2–8 players. You are not heroes. You are peasants called up for the levy, thrown into huge, physics-driven medieval battles with low survival odds. Between campaigns you limp home, patch up your wounds, and slowly grow a camp of tents into a village. Tone: comedy-gruesome, stylized-realistic (not low poly).

Path: game jam vertical slice → Steam release.

## Pillars

1. **Physics combat is the star.** Mount & Blade-style directional attacks, fully simulated: blades get stuck in shields, cut through limbs, and knock people over (active ragdoll). It should be goofy.
2. **Life is cheap, your bloodline isn't.** Wounds are permanent, death is real, and your family and village carry on.
3. **History is the stage, not the script.** The war plays out as it really did. Your story is what happens in your corner of the field.
4. **Funny with friends.** Proximity voice, co-op surgery, looting arguments, terrible homemade gear.

## Setting

- **Decided:** the base game is the Hundred Years' War (1337–1453). The group picks a side (England/France) and a home region.
- Plenty of historical content: Sluys, Crécy, siege of Calais, Neville's Cross, Poitiers, Combat of the Thirty, Auray, Nájera, La Rochelle, Agincourt, Verneuil, Orléans, Patay, Formigny, Castillon. Chevauchées, raids, sieges and skirmishes can fill the gaps procedurally.
- **Black Death (1347–51)** as a world event: villagers die, wages rise, and there is plague-doctor gameplay.
- **Later / DLC:** Scottish Wars of Independence, Wars of the Roses, Reconquista, Hussite Wars, Crusades. More nations and wars ship as expansions.

### Fixed history vs. winning (Open, proposed approach)
- The macro outcome is fixed. Each battle gives your group **personal objectives** in your sector that can be won or lost: hold the ford, take the banner, ransom a named knight, get the wounded out, survive.
- Your rewards come from your performance, not the side's result. Losing at Agincourt but dragging a ransomed English knight home is a triumph.
- Defeats are dramatic gameplay in their own right: the rout, retreat, and escape.
- Procedural skirmishes between historical battles can be truly won or lost.

## Art direction

- **Decided:** TABS-like shapes and simplicity (Totally Accurate Battle Simulator), but with natural skin tones and muted medieval clothing instead of team colours.
- Characters: a few smooth chunky shapes, mostly solid-colour materials, big simple heads, tiny dot eyes, simple hair/beard shapes, stubby hands, floppy limbs. Proportions vary wildly (character creator).
- Environment is richer than TABS: rolling terrain, stylized grass and foliage, soft fog and light.
- Reference concepts: `art/concept/batch04/` (lineup and battle) and `art/concept/batch03/04_field_surgery.png`.
- Concept art is generated with `tools/gen_concept.py` (default model `gpt-image-2.5-sunburst`).

## Core loop (yearly)

- **Spring/summer:** campaign season. The herald arrives, you have a few days to muster, then march, battle, loot, and come home.
- **Harvest/autumn:** farming, taxes, the tithe.
- **Winter:** home, healing, crafting, hunger.

### The call to arms
- A herald rides in and rings the bell. You have N days to muster.
- No-show: a fine. If you can't pay → hanged in the town square.
- **Decided: desertion** mid-battle is a real way to save your character. Run to the edge of the map and you're out; nobody chases you.
  - Cost: no pay, no loot, no ransom from that battle.
  - Risk: a chance the commanders find out. Days later, soldiers arrive at the camp unannounced and take you away for trial.
  - That becomes a side quest for your friends: break you out, bribe the judge, or let justice (or execution) happen. Multiple approaches for variety.
  - If you escape justice, you're demoted in rank for the next battles.

### Battle
- 100v100+ NPCs plus players. Players roam and help; no command until high rank.
- Proximity voice for players. NPC barks via TTS + our own recorded grunts.
- After the battle: **loot the dead** (boots, helmets, coin purses).
- **Ransom:** knock down a knight, drag him back alive, collect a fortune. Captured commoners become village labour.
- Formation-keeping rewards: **dropped.**

### Wounds, surgery, prosthetics
- Per-limb damage → wounds → infection → gangrene → amputation.
- Co-op surgery (ale as anaesthetic, a friend holds the saw).
- Effects: no arm = one-handed only; no eye = narrower FOV; no legs = crutches or…
- **Homemade wheelchairs/carts.** A friend pushes while you fight, or you pick between moving and swinging. Later: donkey-pulled.
- Prosthetics are crafted and grounded medieval (wooden legs, strapped hooks, crutches). Avoid pirate vibes.

### Death & inheritance
- **Decided:** permadeath per character. The next character is a relative (sibling, cousin, child) who inherits the village, part of the gold, and maybe one heirloom. Skills and rank reset.
- The relative's looks are a **random mutation of the founder's design** (weird characters breed weird families).
- A graveyard with headstones and cause of death.
- The village persists even if everyone dies.

### Character creation
- **Decided:** looks are player-designed (blendshapes + bone scaling, so goofy proportions are possible).
- Backstory, traits and starting stats are random, with a reroll.
- **Open:** side/region pick (host chooses at campaign start) vs. random assignment.

### Progression
Gold from surviving, loot and ransom → gear (buy in cities or craft) → ranks: levy → archer/man-at-arms → mounted → knight/noble → eventually commanding troops and influencing politics.

### Crafting
Weapon/armour stats derive from the physics of the shape (mass, balance, reach, edge). Silly weapons emerge naturally.

### Village
Tents → village. Chop wood, farm, fish, hunt, gather herbs, brew remedies, treat wounds. Visitors and merchants. NPC villagers: rescued folk, prisoners.

## Game jam scope (vertical slice)

One full loop and nothing else:
1. Small camp: chop wood, eat, bandage.
2. The herald arrives.
3. One battle, ~100v100 plus players, physics melee.
4. Loot, go home, heal (or die and return as a relative).

Success = physics melee is fun and funny with friends.

Cut for the jam: building, farming, crafting, ranks, horses, character creator depth, campaign map.

## Tech stack

- **Decided: Unreal Engine 5.8.** Chosen over Unity to avoid ~€275 of paid assets; everything below is built in or free.
- **Code:** C++ for core systems (combat, health/wounds, networking, AI) so they live as reviewable text in git. Blueprints only for thin glue and content, edited via Epic's Unreal Engine MCP plugin.
- **Networking:** Unreal's built-in replication, listen server (host-authoritative), Steam via Online Subsystem Steam. Host resolves hits; ragdoll flailing is cosmetic per client where possible ("sync the pelvis + gameplay events").
- **Movement: Mover first** (Network Prediction rollback, Chaos-physics-friendly), copying GASP 5.8's Mover/physics setup as the starting point. Fallback to CharacterMovementComponent if Mover fails the first networked prototype (two players hitting each other online).
- **GASP usage:** start from an empty C++ third-person project; migrate parts from GASP (animations, Mover setup, Physics Control, ragdoll get-ups). Don't build on top of the demo project itself.
- **Voice:** built-in VOIP over Steam with distance attenuation for proximity chat.
- **Physics characters:** Chaos physics + Physics Control Component (active ragdoll; experimental in 5.8) + Control Rig / full-body IK. Reference: Game Animation Sample Project (GASP).
- **Dismemberment:** pre-split limb meshes with cap meshes, swapped at joints (no runtime slicing).
- **Crowd LOD:** full active ragdoll near players → simple animated NPCs mid-range → Mass Entity crowds with baked animation far away → abstract simulation for off-screen formations.
- **Art pipeline:** concept art via OpenAI image gen → base character built in Blender (blendshapes) → props/weapons via Tripo, cleaned in Blender → free PBR textures (Poly Haven, ambientCG) + a stylized shader.
- **Animation:** GASP / Mixamo (free) for locomotion, plus a melee combat pack if needed. Procedural layer via Physics Control and Control Rig.
- **Audio:** OpenAI TTS for NPC barks; our own recorded grunts and screams.
- **Tooling/harness:** Git + Git LFS; Epic's Unreal Engine MCP plugin so Claude can drive the editor; Blender MCP for scripted asset work; computer-use for visual checks of the running game.
