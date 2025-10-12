advancement revoke @s only halloweendeco:events/on_hurt

execute positioned as @s rotated as @s anchored eyes positioned ^ ^ ^2 as @n[type=interaction,tag=deco_triggerbox,distance=..2,nbt={attack:{}}] positioned as @s as @n[type=interaction,tag=deco_origin,distance=..2] run function halloweendeco:destroy_deco with entity @s data