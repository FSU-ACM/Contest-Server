from app import app

@app.template_filter('alert')
def map_flash_category(s):
    return {
        'success': 'success',
        'message': 'info',
        'error': 'danger',
    }.get(s)
