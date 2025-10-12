advancement revoke @s only halloweendeco:events/on_place

execute positioned as @s rotated as @s anchored eyes positioned ^ ^ ^2 as @n[type=armor_stand,predicate=halloweendeco:is_wearing_deco,distance=..2] positioned as @s run function halloweendeco:setup_deco with entity @s equipment.chest.components.minecraft:custom_data