from django.db import models


# Create your models here.


class Clients(models.Model):
    first_name = models.CharField(verbose_name="Имя", max_length=300)
    last_name = models.CharField(verbose_name="Фамилия", max_length=300)
    middle_name = models.CharField(verbose_name="Отчетство", max_length=300)
    email = models.CharField(verbose_name="Email", max_length=100)
    phone = models.CharField(verbose_name="Телефон", max_length=20)
    income = models.DecimalField(verbose_name="Доход", max_digits=15, decimal_places=2)
    family_income = models.DecimalField(verbose_name="Семейный доход", max_digits=15, decimal_places=2)

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class DocTypes(models.Model):
    name = models.CharField(verbose_name="Тип документа", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип документа"
        verbose_name_plural = "Типы документа"


class ClientsDocuments(models.Model):
    name = models.CharField(verbose_name="Имя документа", max_length=300)
    doc_type = models.ForeignKey(DocTypes,
                                 verbose_name='Тип документа',
                                 related_name="doc_type_documents",
                                 on_delete=models.SET_NULL,
                                 null=True)
    client = models.ForeignKey(Clients,
                               verbose_name='Клиент',
                               related_name="client_documents",
                               on_delete=models.SET_NULL,
                               null=True
                               )
    file = models.FileField(verbose_name='Файл документа', upload_to='documents/')
    is_checked = models.BooleanField(verbose_name="Проверено?", default=False)
    change_date = models.DateField(verbose_name="Дата изменения документа", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class InsuranceTypes(models.Model):
    name = models.CharField(verbose_name="Тип страхования", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип страхования"
        verbose_name_plural = "Типы страхования"


class InsuranceVendors(models.Model):
    name = models.CharField(verbose_name="Страховая компания", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страховая компания"
        verbose_name_plural = "Страховые компании"


class InsuranceObjects(models.Model):
    name = models.CharField(verbose_name="Объект страхования", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Объект страхования"
        verbose_name_plural = "Объекты страхования"


class Currencies(models.Model):
    name = models.CharField(verbose_name="Название", max_length=300)
    symbol = models.CharField(verbose_name="Символ", max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"


class VehicleStates(models.Model):
    name = models.CharField(verbose_name="Название состояния авто", max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Состояние автомобиля"
        verbose_name_plural = "Состояния автомобиля"


class VehicleDealers(models.Model):
    name = models.CharField(verbose_name="Название дилера", max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Название дилера"
        verbose_name_plural = "Названия дилеров"


class VehicleModels(models.Model):
    name = models.CharField(verbose_name="Модель", max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Модель авто"
        verbose_name_plural = "Модели авто"


class IncomeProofTypes(models.Model):
    name = models.CharField(verbose_name="Название способа", max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Способ подтверждения дохода"
        verbose_name_plural = "Способы подтверждения дохода"


class CreditPrograms(models.Model):
    name = models.CharField(verbose_name="Название", max_length=300)
    loan_size = models.DecimalField(verbose_name="Размер кредита", max_digits=15, decimal_places=2)
    period = models.IntegerField(verbose_name="Длительность в месяцах")
    init_payment = models.DecimalField(verbose_name="Первоначальный взнос", max_digits=15, decimal_places=2)
    income_proof_type = models.ForeignKey(IncomeProofTypes,
                                          verbose_name="Способ подтверждения дохода",
                                          related_name="income_proof_type_credit_programs",
                                          on_delete=models.SET_NULL,
                                          null=True)
    currency = models.ForeignKey(Currencies,
                                 verbose_name="Валюта",
                                 related_name="currency_credit_programs",
                                 on_delete=models.SET_NULL,
                                 null=True)
    vehicle_state = models.ForeignKey(VehicleStates,
                                      verbose_name="Состояние авто",
                                      related_name="vehicle_state_credit_programs",
                                      on_delete=models.SET_NULL,
                                      null=True)
    interest_rate = models.DecimalField("Процентная ставка", max_digits=5, decimal_places=2)
    commission = models.DecimalField(verbose_name="Комиссия за выдачу кредита", max_digits=15, decimal_places=2)
    early_repayment = models.BooleanField(verbose_name="Возможность досрочного погашения", default=False)
    early_repayment_commission = models.DecimalField("Комиссия за досрочное погашение",
                                                     max_digits=5,
                                                     decimal_places=2,
                                                     null=True)
    use_family_income = models.BooleanField(verbose_name="Использовать семейный доход", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Кредитная программа"
        verbose_name_plural = "Кредитные программы"


class PaymentCalculationType(models.Model):
    name = models.CharField(verbose_name="Название способа", max_length=300)
    credit_programm = models.ForeignKey(CreditPrograms,
                                        verbose_name="Кредитная программа",
                                        related_name="credit_program_payment_calculation_types",
                                        on_delete=models.SET_NULL,
                                        null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Способ расчета ежемесячного платежа"
        verbose_name_plural = "Способы расчета ежемесячного платежа"


class SpecialConditions(models.Model):
    name = models.CharField(verbose_name="Название специального условия", max_length=300)
    credit_programm = models.ForeignKey(CreditPrograms,
                                        verbose_name="Кредитная программа",
                                        related_name="credit_program_special_conditions",
                                        on_delete=models.SET_NULL,
                                        null=True)
    vehicle_dealer = models.ForeignKey(VehicleDealers,
                                       verbose_name="Автодилер",
                                       related_name="vehicle_dealer_special_conditions",
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True)
    insurance_vendor = models.ForeignKey(InsuranceVendors,
                                         verbose_name="Страховая компания",
                                         related_name="insurance_vendor_special_conditions",
                                         on_delete=models.SET_NULL,
                                         null=True,
                                         blank=True)
    vehicle_model = models.ForeignKey(VehicleModels,
                                      verbose_name="Модель Авто",
                                      related_name="vehicle_model_special_conditions",
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True)
    condition = models.CharField(verbose_name="Содержание спец условия", max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Специальное условие"
        verbose_name_plural = "Специальные условия"


class MandatoryDocuments(models.Model):
    name = models.CharField(verbose_name="Название обязательного документа", max_length=300)
    credit_programm = models.ForeignKey(CreditPrograms,
                                        verbose_name="Кредитная программа",
                                        related_name="credit_program_mandatory_docs",
                                        on_delete=models.SET_NULL,
                                        null=True)
    document_type = models.ForeignKey(DocTypes,
                                      verbose_name="Тип документа",
                                      related_name="document_type_mandatory_docs",
                                      on_delete=models.SET_NULL,
                                      null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Обязательный документ"
        verbose_name_plural = "Обязательные документы"


class MandatoryInsurances(models.Model):
    name = models.CharField(verbose_name="Название", max_length=300)
    credit_programm = models.ForeignKey(CreditPrograms,
                                        verbose_name="Кредитная программа",
                                        related_name="credit_program_mandatory_insurances",
                                        on_delete=models.SET_NULL,
                                        null=True)
    insurance_type = models.ForeignKey(InsuranceTypes,
                                       verbose_name="Тип страхования (обязательный/опциональный)",
                                       related_name="insurance_type_mandatory_insurances",
                                       on_delete=models.SET_NULL,
                                       null=True)
    insurance_object = models.ForeignKey(InsuranceObjects,
                                         verbose_name="Объект страхования",
                                         related_name="insurance_object_mandatory_insurances",
                                         on_delete=models.SET_NULL,
                                         null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Обязательное страхование"
        verbose_name_plural = "Обязательные страхования"


class Credits(models.Model):
    client = models.ForeignKey(Clients,
                               verbose_name="Клиент",
                               related_name="client_credits",
                               on_delete=models.SET_NULL,
                               null=True)
    guarantor = models.ForeignKey(Clients,
                                  verbose_name="Поручитель",
                                  related_name="guarantor_credits",
                                  on_delete=models.SET_NULL,
                                  null=True)
    credit_program = models.ForeignKey(CreditPrograms,
                                       verbose_name="Кредитная программа",
                                       related_name="credit_program_credits",
                                       on_delete=models.SET_NULL,
                                       null=True)
    loan_size = models.DecimalField(verbose_name="Размер кредита", max_digits=15, decimal_places=2)
    period = models.IntegerField(verbose_name="Длительность в месяцах")
    init_payment = models.DecimalField(verbose_name="Первоначальный взнос", max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField("Процентная ставка", max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Кредит"
        verbose_name_plural = "Кредиты"


class Insurances(models.Model):
    name = models.CharField(verbose_name="Название", max_length=300)
    credit = models.ForeignKey(Credits,
                               verbose_name="Кредит",
                               related_name="credit_insurances",
                               on_delete=models.SET_NULL,
                               null=True
                               )
    insurance_type = models.ForeignKey(InsuranceTypes,
                                       verbose_name="Тип страхования",
                                       related_name="types_insurances",
                                       on_delete=models.SET_NULL,
                                       null=True)
    insurance_object = models.ForeignKey(InsuranceObjects,
                                         verbose_name="Объект страхования",
                                         related_name="objects_insurances",
                                         on_delete=models.SET_NULL,
                                         null=True)
    client = models.ForeignKey(Clients,
                               verbose_name="Клиент",
                               related_name="clients_insurances",
                               on_delete=models.SET_NULL,
                               null=True)
    insurance_vendor = models.ForeignKey(InsuranceVendors,
                                         verbose_name="Страховая компания",
                                         related_name="vendors_insurances",
                                         on_delete=models.SET_NULL,
                                         null=True)
    date_from = models.DateTimeField(verbose_name="Дата начала действия страхования")
    date_to = models.DateTimeField(verbose_name="Дата окончания действия страхования")
    document = models.FileField(verbose_name='Файл документа', upload_to='documents/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страхование"
        verbose_name_plural = "Страхование"


class PaymentConditions(models.Model):
    name = models.CharField(verbose_name="Название состояния платежа", max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Состояние платежа"
        verbose_name_plural = "Состояния платежей"


class PaymentChangeReasons(models.Model):
    name = models.CharField(verbose_name="Причина изменения графика платежей", max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Причина изменения в графике платежей"
        verbose_name_plural = "Причины изменения в графике платежей"


class PaymentSchedules(models.Model):
    credit = models.ForeignKey(Credits,
                               verbose_name="Кредит",
                               related_name="credit_payment_schedules",
                               on_delete=models.SET_NULL,
                               null=True)
    date = models.DateTimeField(verbose_name="Дата платежа")
    main_payment_amount = models.DecimalField(verbose_name="Основной долг", max_digits=15, decimal_places=2)
    percents_payment_amount = models.DecimalField(verbose_name="Процент на остаток", max_digits=15, decimal_places=2)
    condition = models.ForeignKey(PaymentConditions,
                                  verbose_name="Состояние платежа",
                                  related_name="condition_payment_schedules",
                                  on_delete=models.SET_NULL,
                                  null=True)
    reason = models.ForeignKey(PaymentChangeReasons,
                               verbose_name="Причина изменения графика",
                               related_name="reason_payment_schedules",
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "График платежа"
        verbose_name_plural = "Графики платежей"


class PaymentDelays(models.Model):
    credit = models.ForeignKey(Credits,
                               verbose_name="Кредит",
                               related_name="credit_payment_delays",
                               on_delete=models.SET_NULL,
                               null=True)
    payment = models.ForeignKey(PaymentSchedules,
                                verbose_name="Платеж",
                                related_name="payment_payment_delays",
                                on_delete=models.SET_NULL,
                                null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Просрочка по платежу"
        verbose_name_plural = "Просрочки по платежу"


class BlackLists(models.Model):
    client = models.ForeignKey(Clients,
                               verbose_name="Клиент",
                               related_name="client_black_lists",
                               on_delete=models.SET_NULL,
                               null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Черный список"
        verbose_name_plural = "Черные списки"