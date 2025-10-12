# Summon item back
$loot spawn ~ ~ ~ loot halloweendeco:$(deco_id)
summon item ~ ~ ~ {Item:{id:"minecraft:armor_stand",count:1}}

# Kill triggerbox, deco origin and all of its children (all related deco model entities)
kill @n[type=interaction,tag=deco_triggerbox,distance=..2,nbt={attack:{}}]
execute on passengers run kill @s
kill @s