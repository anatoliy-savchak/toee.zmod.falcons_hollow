# AnimGoalType
AG_ANIMATE = 0 # 0x0
AG_ANIMATE_LOOP = 1 # 0x1
AG_ANIM_IDLE = 2 # 0x2
AG_ANIM_FIDGET = 3 # 0x3
AG_MOVE_TO_TILE = 4 # 0x4
AG_RUN_TO_TILE = 5 # 0x5
AG_ATTEMPT_MOVE = 6 # 0x6
AG_MOVE_TO_PAUSE = 7 # 0x7
AG_MOVE_NEAR_TILE = 8 # 0x8
AG_MOVE_NEAR_OBJ = 9 # 0x9
AG_MOVE_STRAIGHT = 10 # 0xA
AG_ATTEMPT_MOVE_STRAIGHT = 11 # 0xB
AG_OPEN_DOOR = 12 # 0xC
AG_ATTEMPT_OPEN_DOOR = 13 # 0xD
AG_UNLOCK_DOOR = 14 # 0xE
AG_JUMP_WINDOW = 15 # 0xF
AG_PICKUP_ITEM = 16 # 0x10
AG_ATTEMPT_PICKUP = 17 # 0x11
AG_PICKPOCKET = 18 # 0x12
AG_ATTACK = 19 # 0x13
AG_ATTEMPT_ATTACK = 20 # 0x14
AG_TALK = 21 # 0x15
AG_PICK_WEAPON = 22 # 0x16
AG_CHASE = 23 # 0x17
AG_FOLLOW = 24 # 0x18
AG_FOLLOW_TO_LOCATION = 25 # 0x19
AG_FLEE = 26 # 0x1A
AG_THROW_SPELL = 27 # 0x1B
AG_ATTEMPT_SPELL = 28 # 0x1C
AG_SHOOT_SPELL = 29 # 0x1D
AG_HIT_BY_SPELL = 30 # 0x1E
AG_HIT_BY_WEAPON = 31 # 0x1F
AG_DODGE = 32 # 0x20
AG_DYING = 33 # 0x21
AG_DESTROY_OBJ = 34 # 0x22
AG_USE_SKILL_ON = 35 # 0x23
AG_ATTEMPT_USE_SKILL_ON = 36 # 0x24
AG_SKILL_CONCEAL = 37 # 0x25
AG_PROJECTILE = 38 # 0x26
AG_THROW_ITEM = 39 # 0x27
AG_USE_OBJECT = 40 # 0x28
AG_USE_ITEM_ON_OBJECT = 41 # 0x29
AG_USE_ITEM_ON_OBJECT_WITH_SKILL = 42 # 0x2A
AG_USE_ITEM_ON_TILE = 43 # 0x2B
AG_USE_ITEM_ON_TILE_WITH_SKILL = 44 # 0x2C
AG_KNOCKBACK = 45 # 0x2D
AG_FLOATING = 46 # 0x2E
AG_CLOSE_DOOR = 47 # 0x2F
AG_ATTEMPT_CLOSE_DOOR = 48 # 0x30
AG_ANIMATE_REVERSE = 49 # 0x31
AG_MOVE_AWAY_FROM_OBJ = 50 # 0x32
AG_ROTATE = 51 # 0x33
AG_UNCONCEAL = 52 # 0x34
AG_RUN_NEAR_TILE = 53 # 0x35
AG_RUN_NEAR_OBJ = 54 # 0x36
AG_ANIMATE_STUNNED = 55 # 0x37
AG_ANIMATE_KNEEL_MAGIC_HANDS = 56 # 0x38
AG_ATTEMPT_MOVE_NEAR = 57 # 0x39
AG_KNOCK_DOWN = 58 # 0x3A
AG_ANIM_GET_UP = 59 # 0x3B
AG_ATTEMPT_MOVE_STRAIGHT_KNOCKBACK = 60 # 0x3C
AG_WANDER = 61 # 0x3D
AG_WANDER_SEEK_DARKNESS = 62 # 0x3E
AG_USE_PICKLOCK_SKILL_ON = 63 # 0x3F
AG_PLEASE_MOVE = 64 # 0x40
AG_ATTEMPT_SPREAD_OUT = 65 # 0x41
AG_ANIMATE_DOOR_OPEN = 66 # 0x42
AG_ANIMATE_DOOR_CLOSED = 67 # 0x43
AG_PEND_CLOSING_DOOR = 68 # 0x44
AG_THROW_SPELL_FRIENDLY = 69 # 0x45
AG_ATTEMPT_SPELL_FRIENDLY = 70 # 0x46
AG_ANIMATE_LOOP_FIRE_DMG = 71 # 0x47
AG_ATTEMPT_MOVE_STRAIGHT_SPELL = 72 # 0x48
AG_MOVE_NEAR_OBJ_COMBAT = 73 # 0x49
AG_ATTEMPT_MOVE_NEAR_COMBAT = 74 # 0x4A
AG_USE_CONTAINER = 75 # 0x4B
AG_THROW_SPELL_W_CAST_ANIM = 76 # 0x4C
AG_ATTEMPT_SPELL_W_CAST_ANIM = 77 # 0x4D
AG_THROW_SPELL_W_CAST_ANIM_2NDARY = 78 # 0x4E
AG_BACK_OFF_FROM = 79 # 0x4F
AG_ATTEMPT_USE_PICKPOCKET_SKILL_ON = 80 # 0x50
AG_USE_DISABLE_DEVICE_SKILL_ON_DATA = 81 # 0x51
AG_COUNT = 82 # 0x52

class WeaponAnim:
    _None = 0
    RightAttack = 1
    RightAttack2 = 2
    RightAttack3 = 3
    LeftAttack = 4
    LeftAttack2 = 5
    LeftAttack3 = 6
    Walk = 7
    Run = 8
    Idle = 9
    FrontHit = 10
    FrontHit2 = 11
    FrontHit3 = 12
    LeftHit = 13
    LeftHit2 = 14
    LeftHit3 = 15
    RightHit = 16
    RightHit2 = 17
    RightHit3 = 18
    BackHit = 19
    BackHit2 = 20
    BackHit3 = 21
    RightCriticalSwing = 22
    LeftCriticalSwing = 23
    Fidget = 24
    Fidget2 = 25
    Fidget3 = 26
    Sneak = 27
    Panic = 28
    RightCombatStart = 29
    LeftCombatStart = 30
    CombatIdle = 31
    CombatFidget = 32
    Special1 = 33
    Special2 = 34
    Special3 = 35
    FrontDodge = 36
    RightDodge = 37
    LeftDodge = 38
    BackDodge = 39
    RightThrow = 40
    LeftThrow = 41
    LeftSnatch = 42
    RightSnatch = 43
    LeftTurn = 44
    RightTurn = 45

class WeaponAnimType:
    Unarmed = 0
    Dagger = 1
    Sword = 2
    Mace = 3
    Hammer = 4
    Axe = 5
    Club = 6
    Battleaxe = 7
    Greatsword = 8
    Greataxe = 9
    Greathammer = 10
    Spear = 11
    Staff = 12
    Polearm = 13
    Bow = 14
    Crossbow = 15
    Sling = 16
    Shield = 17
    Flail = 18
    Chain = 19
    TwoHandedFlail = 20
    Shuriken = 21
    Monk = 22

class NormalAnimType:
    Falldown = 0
    ProneIdle = 1
    ProneFidget = 2
    Getup = 3
    Magichands = 4
    Picklock = 5
    PicklockConcentrated = 6
    Examine = 7
    Throw = 8
    Death = 9
    Death2 = 10
    Death3 = 11
    DeadIdle = 12
    DeadFidget = 13
    DeathProneIdle = 14
    DeathProneFidget = 15
    AbjurationCasting = 16
    AbjurationConjuring = 17 # errorneus for human
    ConjurationCasting = 18
    ConjurationConjuring = 19 # errorneus for human
    DivinationCasting = 20
    DivinationConjuring = 21 # errorneus for human
    EnchantmentCasting = 22
    EnchantmentConjuring = 23 # errorneus for human
    EvocationCasting = 24
    EvocationConjuring = 25 # errorneus for human
    IllusionCasting = 26
    IllusionConjuring = 27 # errorneus for human
    NecromancyCasting = 28
    NecromancyConjuring = 29 # errorneus for human
    TransmutationCasting = 30
    TransmutationConjuring = 31 # errorneus for human
    Conceal = 32
    ConcealIdle = 33
    Unconceal = 34
    ItemIdle = 35
    ItemFidget = 36
    Open = 37
    Close = 38
    SkillAnimalEmpathy = 39
    SkillDisableDevice = 40
    SkillHeal = 41
    SkillHealConcentrated = 42
    SkillHide = 43
    SkillHideIdle = 44
    SkillHideFidget = 45
    SkillUnhide = 46
    SkillPickpocket = 47
    SkillSearch = 48
    SkillSpot = 49
    FeatTrack = 50
    Trip = 51 
    Bullrush = 52 # errorneus for human
    Flurry = 53
    Kistrike = 54
    Tumble = 55 # errorneus for human
    Special1 = 56 # errorneus for human
    Special2 = 57 # errorneus for human
    Special3 = 58 # errorneus for human
    Special4 = 59 # errorneus for human
    Throw2 = 60
    WandAbjurationCasting = 61
    WandAbjurationConjuring = 62
    WandConjurationCasting = 63
    WandConjurationConjuring = 64
    WandDivinationCasting = 65
    WandDivinationConjuring = 66
    WandEnchantmentCasting = 67
    WandEnchantmentConjuring = 68
    WandEvocationCasting = 69
    WandEvocationConjuring = 70
    WandIllusionCasting = 71
    WandIllusionConjuring = 72
    WandNecromancyCasting = 73
    WandNecromancyConjuring = 74
    WandTransmutationCasting = 75
    WandTransmutationConjuring = 76
    SkillBarbarianRage = 77
    OpenIdle = 78