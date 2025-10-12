# Summon origin point to parent all other entities (excluding triggerbox)
$summon interaction ~ ~ ~ {width:0,height:0,Tags:[deco_origin],data:{deco_id:$(deco_id)}}

# Spawn deco model & hitbox
$function halloweendeco:spawn/$(deco_id)
$summon interaction ~ ~ ~ {width:$(deco_width),height:$(deco_height),Tags:[deco_triggerbox]}

# Rotate deco
execute as @e[type=!player,type=!minecraft:armor_stand,distance=..1.2] positioned as @s facing entity @p feet run rotate @s ~ 0

# Remove armor stand
kill @n[type=armor_stand,predicate=halloweendeco:is_wearing_deco]

# Tag all of the model entities
execute as @n[tag=deco_parent,distance=..2] on passengers run tag @s add deco_part

# Dismount and remount all model entities
execute as @e[tag=deco_part,distance=..2] run ride @s dismount
execute as @e[tag=deco_part,distance=..2] run ride @s mount @n[tag=deco_origin,distance=..2]
ride @n[tag=deco_parent,distance=..2] mount @n[tag=deco_origin,distance=..2]

# Remove tagging
execute as @n[tag=deco_parent,distance=..2] on passengers run tag @s remove deco_part