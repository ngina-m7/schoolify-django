# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, choices=USER_TYPE_CHOICES, max_length=10)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    position = models.CharField(max_length=255)  # Add more fields as needed
    objects = models.Manager()


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_birth = models.DateField()
    class_enrolled = models.CharField(max_length=255)
    address = models.TextField()
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    objects = models.Manager()


class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    students_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance = models.ForeignKey('Attendance', on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    report_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StudentLeaveReport(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    leave_date = models.DateField()
    message = models.TextField()
    status = models.CharField(max_length=255)  # 'Pending', 'Approved', 'Rejected'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StaffLeaveReport(models.Model):
    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE)
    leave_date = models.DateField()
    message = models.TextField()
    status = models.CharField(max_length=255)  # 'Pending', 'Approved', 'Rejected'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StudentFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE)
    feedback = models.TextField()  # Assuming feedback is text
    feedback_reply = models.TextField()  # Assuming feedback reply is text
    feedback_date = models.DateField(auto_now_add=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StaffFeedback(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey('Staff', on_delete=models.CASCADE)
    feedback = models.TextField()  # Assuming feedback is text
    feedback_reply = models.TextField()  # Assuming feedback reply is text
    feedback_date = models.DateField(auto_now_add=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StudentNotification(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey('Student', on_delete=models.CASCADE)
    message = models.TextField()  # Assuming message is text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class StaffNotification(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey('Staff', on_delete=models.CASCADE)
    message = models.TextField()  # Assuming message is text
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


from django.dispatch import receiver
from django.db.models.signals import post_save
from student_management_app.models import CustomUser, AdminHOD, Staff, Student

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profiles(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        elif instance.user_type == 2:
            Staff.objects.create(admin=instance)
        elif instance.user_type == 3:
            Student.objects.create(admin=instance)
    else:
        if instance.user_type == 1:
            AdminHOD.objects.filter(admin=instance).update(admin=instance)
        elif instance.user_type == 2:
            Staff.objects.filter(admin=instance).update(admin=instance)
        elif instance.user_type == 3:
            Student.objects.filter(admin=instance).update(admin=instance)


