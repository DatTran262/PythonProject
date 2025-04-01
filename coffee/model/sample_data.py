from .menu_repository import MenuRepository

SAMPLE_MENU_ITEMS = [
    {
        'name': 'Cà phê đen',
        'description': 'Cà phê đen truyền thống',
        'price': 20000,
        'category': 'Cà phê'
    },
    {
        'name': 'Cà phê sữa',
        'description': 'Cà phê sữa đặc thơm ngon',
        'price': 25000,
        'category': 'Cà phê'
    },
    {
        'name': 'Bạc xỉu',
        'description': 'Cà phê sữa tươi thơm béo',
        'price': 30000,
        'category': 'Cà phê'
    },
    {
        'name': 'Trà đào',
        'description': 'Trà đào cam sả mát lạnh',
        'price': 35000,
        'category': 'Trà'
    },
    {
        'name': 'Trà vải',
        'description': 'Trà vải thanh mát',
        'price': 35000,
        'category': 'Trà'
    },
    {
        'name': 'Bánh flan',
        'description': 'Bánh flan thơm béo',
        'price': 15000,
        'category': 'Bánh'
    },
    {
        'name': 'Tiramisu',
        'description': 'Bánh tiramisu Ý',
        'price': 35000,
        'category': 'Bánh'
    }
]

def create_sample_menu_items():
    """Create sample menu items in database"""
    menu_repo = MenuRepository()
    for item in SAMPLE_MENU_ITEMS:
        menu_repo.save_item(item)