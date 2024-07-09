# coding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import os
from django.db import models
from django.utils import timezone
from card_db.settings import MEDIA_ROOT

# This file describes the models off of which the database tables
# will be based


LOCATION_LENGTH = 100            # Constant for maximum location size
MAX_COMMENT_LENGTH = 1000        # Constant for max comment length



def validate_card_id(value):
    """ This determines whether an input card ID is valid """
    
    # ID must be a string of digits
    if not value.isdigit():
        raise ValidationError('ID must only contain numbers')

    # ID must be 7 digits long
    if len(value) != 7:
        raise ValidationError('ID must be 7 digits long')

    curId = value[(len(value) - 3):]
    sameId = QieCard.objects.filter(barcode__iendswith=curId).exclude(barcode__exact=value)
    
    # Last 3 digits of ID must be unique
    if sameId:
        raise ValidationError(
            ('Card "%(value)s" is already recorded'),
            params={'value':curId},
        )
        

def validate_uid(uid):
    """ This determines whether a card UID is valid """
    
    parsed = uid.split(":")
    
    if uid == "":
        return ""
    
    #UID must have 6 sections
    if not len(parsed) == 6:
        raise ValidationError("UID must have six ':'-separated sections")
        
    for part in parsed:
    
        # All UID sections must have 2 characters
        if not len(part) == 2:
            raise ValidationError("Each section must contain two characters")
        for letter in part:
            
            # All characters in the UID must be valid hexadecimal digits
            if not letter.isdigit() and not (letter.lower() >= 'a' and letter.lower() <= 'f'):
                raise ValidationError("UID may only contain hexadecimal digits")


class Test(models.Model):
    """ This model stores information about each type of test """
    
    name            = models.CharField(max_length=100, default="")
    abbreviation    = models.CharField(max_length=100, default="", unique=True)
    description     = models.TextField(max_length=1500, default="")
    required        = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Tester(models.Model):
    """ This model stores information about the testers of the cards """

    username    = models.CharField(max_length=100, default="", unique=True)
    email       = models.EmailField(max_length=255)
    affiliation = models.CharField('Affiliation', max_length=200, default="") 

    def __str__(self):
       return self.username


class QieCard(models.Model):
    """ This model stores information about the different QIE cards """
    
    barcode = models.CharField(max_length=7, validators=[validate_card_id], unique=True, default="")
    uid     = models.CharField(max_length=21, blank=True, default="")
    bridge_major_ver    = models.CharField(max_length=4, default="", blank=True)
    bridge_minor_ver    = models.CharField(max_length=4, default="", blank=True)
    bridge_other_ver    = models.CharField(max_length=8, default="", blank=True)
    igloo_major_ver     = models.CharField(max_length=4, default="", blank=True)
    igloo_minor_ver     = models.CharField(max_length=4, default="", blank=True)
    comments    = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True, default="")

    def get_uid_flipped(self):
        familyName = self.uid[8:16]
        checkSum = self.uid[0:8]
        return "0x" + familyName + " 0x" + checkSum
    
    def get_uid_mac(self):
        """ Parses the raw UID into a mac-address format """
        raw = self.uid[2:]
        refined = ""
        for i in range(6):
            refined += raw[2*i : 2*(i + 1)]
            refined += ':'
        return refined[:17]

    def get_bar_uid(self):
        """ Returns the unique 3-digit code of this card's ID """
        return self.barcode[(len(self.barcode) - 3):]

    def get_bridge_ver(self):
        if self.bridge_major_ver == "" or self.bridge_minor_ver == "" or self.bridge_other_ver == "":
            return "Not Uploaded" 
        major = str(int(self.bridge_major_ver, 16))
        minor = str(int(self.bridge_minor_ver, 16))
        other = str(int(self.bridge_other_ver, 16))
        return major + "." + minor + "." + other
  
    def get_igloo_ver(self):
        if self.igloo_major_ver == "" or self.igloo_minor_ver == "":
            return "Not Uploaded" 
        major = str(int(self.igloo_major_ver, 16))
        minor = str(int(self.igloo_minor_ver, 16))
        return major + "." + minor 

    def __str__(self):
       return str(self.barcode)

        
def images_location(upload, original_filename):
    cardName    = str(QieCard.objects.get(pk=upload.barcode).barcode) + "/"
    testAbbrev  = str(Test.objects.get(pk=upload.test_type_id).abbreviation) + "/"
    attemptNum  = str(upload.attempt_number) + "/"
    
    return os.path.join("images/", cardName, testAbbrev, attemptNum, original_filename)
    
def logs_location(upload, original_filename):
    cardName    = str(QieCard.objects.get(pk=upload.barcode).barcode) + "/"
    testAbbrev  = str(Test.objects.get(pk=upload.test_type_id).abbreviation) + "/"
    attemptNum  = str(upload.attempt_number) + "/"
    
    return os.path.join("uploads/", "user_uploaded_logs/", cardName, testAbbrev, attemptNum, original_filename)
        
class Attempt(models.Model):
    """ This model stores information about each testing attempt """

    card        = models.ForeignKey(QieCard, on_delete=models.CASCADE)      # The card this attempt was on
    plane_loc   = models.CharField(max_length=LOCATION_LENGTH, default="")
    test_type   = models.ForeignKey(Test, on_delete=models.PROTECT)         # The test this attempt was of
    attempt_number  = models.IntegerField(default=1)
    tester      = models.ForeignKey(Tester, on_delete=models.PROTECT)       # the person who enterd this attempt
    date_tested = models.DateTimeField('date tested')
    num_passed  = models.IntegerField(default=-1)
    num_failed  = models.IntegerField(default=-1)
    revoked     = models.BooleanField(default=False)
    overwrite_pass  = models.BooleanField(default=False)
    temperature = models.FloatField(default=-999.9)
    humidity    = models.FloatField(default=-999.9)
    comments    = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True, default="")
    image       = models.ImageField(upload_to=images_location, default="default.png")
    
    log_file        = models.FileField(upload_to=logs_location, default='default.png')
    log_comments    = models.TextField(max_length=MAX_COMMENT_LENGTH, blank=True, default="")
    
    hidden_log_file = models.FileField(upload_to=logs_location, default='default.png')
    
    def passed_all(self):
        return (self.num_failed == 0)

    def has_image(self):
        """ This returns whether the attempt has a specified image """
        return (not self.image == "default.png")
        
    def has_log(self):
        """ This returns whether the attempt has a log folder """
        return (not self.log_file == "default.png")

    def get_status(self):
        if self.revoked:
            return "REVOKED"
        elif self.overwrite_pass:
            return "PASS (FORCED)"
        elif self.num_failed == 0:
            return "PASS"
        else:
            return "FAIL"

    def get_css_class(self):
        """ This returns the color which the Attempt template should take """
        if self.revoked:
            return "warn"
        elif self.overwrite_pass:
            return "forced"
        elif self.num_failed == 0:
            return "okay"
        else:
            return "bad"

    def get_images(self):
        path = MEDIA_ROOT + str(self.image)
        #images = [image for image in os.listdir(os.path.join(MEDIA_ROOT, self.image.url))]
        if not str(self.image)[-4:] == "uhtr" and not str(self.image)[-4:] == "r.gz":
            return os.listdir(path)

    def __str__(self):
        return str(self.test_type)


class ReadoutModule(models.Model):
    
    ODU_TYPE_OPTIONS = [
                        ("1-3", "1-3"),
                        ("2-4", "2-4"),
                        ]
    
    assembler   = models.CharField('Assembler', max_length=50, default="")
    date        = models.DateTimeField('Date Received', default=timezone.now)
    rm_number   = models.IntegerField('RM №', default=-1)
    card_pack_number    = models.IntegerField('CardPack №', default=-1)
    card_1  = models.ForeignKey(QieCard, verbose_name='QIE card 1 №', related_name="rm_1", on_delete=models.PROTECT)
    card_2  = models.ForeignKey(QieCard, verbose_name='QIE card 2 №', related_name="rm_2", on_delete=models.PROTECT)
    card_3  = models.ForeignKey(QieCard, verbose_name='QIE card 3 №', related_name="rm_3", on_delete=models.PROTECT)
    card_4  = models.ForeignKey(QieCard, verbose_name='QIE card 4 №', related_name="rm_4", on_delete=models.PROTECT)
    mtp_optical_cable   = models.CharField('1 MTP to 8 LC optical cable №', max_length=50, default="")
    sipm_control_card   = models.IntegerField('1 SiPM Control Card with BV mezzanine №', default=-1)
    sipm_array_1    = models.IntegerField('SiPM Array S10943-4732 № (BV1-8)', default=-1)
    sipm_array_2    = models.IntegerField('SiPM Array S10943-4732 № (BV17-24)', default=-1)
    sipm_array_3    = models.IntegerField('SiPM Array S10943-4732 № (BV25-32)', default=-1)
    sipm_array_4    = models.IntegerField('SiPM Array S10943-4732 № (BV33-40)', default=-1)
    sipm_array_5    = models.IntegerField('SiPM Array S10943-4732 № (BV41-48)', default=-1)
    mixed_sipm_array    = models.IntegerField('Mixed SiPM array S10943-4733 № (BV9-16)', default=-1)
    odu_type    = models.CharField('ODU type', choices=ODU_TYPE_OPTIONS, max_length=3, default="")
    odu_number  = models.IntegerField('ODU №', default=-1)
    minsk       = models.IntegerField('White box with RM mechanics from Minsk №', default=-1)


class Location(models.Model):
    """ This model stores information about a particular location where a card has been """
    
    card = models.ForeignKey(QieCard, on_delete=models.CASCADE)
    date_received = models.DateTimeField('date received', default=timezone.now)
    geo_loc = models.CharField('Location',max_length=200, default="")

# An appendage to the save function
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


class QieShuntParams(models.Model):
    card    = models.ForeignKey(QieCard, on_delete=models.CASCADE)
    serial  = models.IntegerField(default=-1)
    qie     = models.IntegerField(default=-1)
    cap_ID  = models.IntegerField(default=-1)
    cal_range   = models.IntegerField(default=-1)
    shunt   = models.DecimalField(max_digits=50, decimal_places=20, default=float('inf'))
    slope   = models.DecimalField(max_digits=50, decimal_places=20, default=float('inf'))
    offset  = models.DecimalField(max_digits=50, decimal_places=20, default=float('inf'))
    date    = models.DateTimeField('date received', default=timezone.now)
    plots   = models.ImageField(upload_to=images_location, default="default.png")
    results_file    = models.FileField(upload_to=logs_location, default='default.png')
    

@receiver(pre_save)
def pre_save_handler(sender, instance, *args, **kwargs):
    instance.full_clean()

# An appendage to the delete function
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
import shutil
from card_db.settings import MEDIA_ROOT


@receiver(pre_delete, sender=Attempt)
def mymodel_delete(sender, instance, **kwargs):
    """ Deletes the stored image """
    if len(Attempt.objects.filter(card=instance.card)) == 1:
        if instance.image != "default.png":
            instance.image.delete(False)
        if instance.log_file != "default.png" and os.path.exists(os.path.join(MEDIA_ROOT, os.path.dirname(instance.log_file.name))):
            shutil.rmtree(os.path.join(MEDIA_ROOT, os.path.dirname(instance.log_file.name)))
