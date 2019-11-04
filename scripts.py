import random
from datacenter.models import Schoolkid, Lesson, Mark, Chastisement, Subject, Commendation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def get_schoolkid_detail(schoolkid):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid)
    except (ObjectDoesNotExist, MultipleObjectsReturned) as ex:
        print('please, specify correct schoolkid name', ex)


def fix_marks(schoolkid):
    try:
        schoolkid_detail = Schoolkid.objects.get(full_name__contains=schoolkid)
        Mark.objects.filter(schoolkid=schoolkid_detail, 
                            points__in=[2,3]).update(points=5)
    except (ObjectDoesNotExist, MultipleObjectsReturned) as ex:
        print('please, specify correct schoolkid name', ex)


def remove_chastisements(schoolkid):
    try:
        schoolkid_detail = Schoolkid.objects.get(full_name__contains=schoolkid)
        Chastisement.objects.filter(schoolkid__full_name__contains=schoolkid).delete()
    except (ObjectDoesNotExist, MultipleObjectsReturned) as ex:
        print('please, specify correct schoolkid name', ex)


def create_commendation(schoolkid, subj):
    commend_list = ['Молодец!',
                    'Отлично!',
                    'Хорошо!',
                    'Гораздо лучше, чем я ожидал!',
                    'Ты меня приятно удивил!',
                    'Великолепно!',
                    'Прекрасно!', 
                    'Ты меня очень обрадовал!',
                    'Именно этого я давно ждал от тебя!']
    try:
        schoolkid_detail = Schoolkid.objects.get(full_name__contains=schoolkid)
        subject = Subject.objects.get(title=subj, year_of_study=schoolkid_detail.year_of_study)
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        print('please, specify correct schoolkid or subject name')
        return
    lessons = Lesson.objects.filter(year_of_study=schoolkid_detail.year_of_study,
                                    group_letter=schoolkid_detail.group_letter,
                                    subject__title=subj).order_by('date') 
    teacher = lessons[0].teacher
    date_commend = lessons[0].date
    comm = Commendation(text=random.choice(commend_list), created=date_commend, schoolkid=schoolkid_detail, subject=subject, teacher=teacher)
    comm.save()

