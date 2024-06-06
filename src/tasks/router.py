from fastapi import APIRouter, BackgroundTasks, Depends

from src.auth.auth import current_user

from .tasks import send_email_report_dashboard

router = APIRouter(prefix="/report")

@router.get('/dashboard')
def get_dashboard(user = Depends(current_user)):
    # background_tasks.add_task(send_email_report_dashboard, user.username) # встроеная тука от пайтона, без селери. В параметрах background_tasks: BackgroundTasks
    # send_email_report_dashboard(user.username) # самый долгий вариант, просто выполнение
    send_email_report_dashboard.delay(user.username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }