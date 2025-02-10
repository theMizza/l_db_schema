import os
import django
from datetime import datetime, timedelta
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()


from app.models import *


def create_test_data():
    print("Start populating db")
    clients = []
    for i in range(1, 21):
        client = Clients.objects.create(
            first_name=f"Имя_{i}",
            last_name=f"Фамилия_{i}",
            middle_name=f"Отчество_{i}",
            email=f"client_{i}@example.com",
            phone=f"+7999{random.randint(1000000, 9999999)}",
            income=random.randint(50000, 300000),
            family_income=random.randint(100000, 500000)
        )
        clients.append(client)

    doc_type1 = DocTypes.objects.create(name="Паспорт")
    doc_type2 = DocTypes.objects.create(name="Водительское удостоверение")

    for client in clients:
        ClientsDocuments.objects.create(
            name=f"Паспорт {client.last_name}",
            doc_type=doc_type1,
            client=client,
            file=f"documents/passport_{client.id}.pdf",
            is_checked=True
        )
        ClientsDocuments.objects.create(
            name=f"Водительское удостоверение {client.last_name}",
            doc_type=doc_type2,
            client=client,
            file=f"documents/driver_license_{client.id}.pdf",
            is_checked=random.choice([True, False])
        )

    credit_programs = []
    for i in range(1, 6):
        use_family_income = random.choice([True, False])
        loan_size = random.randint(500000, 2000000)
        credit_program = CreditPrograms.objects.create(
            name=f"Кредитная программа {i}",
            loan_size=loan_size,
            period=random.randint(12, 60),
            init_payment=random.randint(50000, 300000),
            income_proof_type=IncomeProofTypes.objects.create(name=f"Способ подтверждения дохода {i}"),
            currency=Currencies.objects.create(name=f"Валюта {i}", symbol="$"),
            vehicle_state=VehicleStates.objects.create(name=f"Состояние авто {i}"),
            interest_rate=random.uniform(8.0, 15.0),
            commission=random.randint(5000, 20000),
            early_repayment=random.choice([True, False]),
            early_repayment_commission=random.uniform(1.0, 3.0) if random.choice([True, False]) else None,
            use_family_income=use_family_income
        )
        credit_programs.append(credit_program)

        MandatoryDocuments.objects.create(
            name=f"Обязательный документ для программы {i}",
            credit_programm=credit_program,
            document_type=random.choice([doc_type1, doc_type2])
        )

    for client in clients:
        credit = Credits.objects.create(
            client=client,
            credit_program=random.choice(credit_programs),
            loan_size=random.randint(500000, 2000000),
            period=random.randint(12, 60),
            init_payment=random.randint(50000, 300000),
            interest_rate=random.uniform(8.0, 15.0)
        )

        for month in range(1, credit.period + 1):
            payment_date = datetime.now() - timedelta(days=30 * month)
            PaymentSchedules.objects.create(
                credit=credit,
                date=payment_date,
                main_payment_amount=credit.loan_size / credit.period,
                percents_payment_amount=(credit.loan_size * credit.interest_rate / 100) / 12,
                condition=PaymentConditions.objects.create(name="Просрочен")
            )

        for payment in PaymentSchedules.objects.filter(credit=credit):
            if random.choice([True, False]):
                PaymentDelays.objects.create(
                    credit=credit,
                    payment=payment
                )

    for client in random.sample(clients, 5):
        BlackLists.objects.create(client=client)

    client_1 = Clients.objects.get(id=1)
    client_1.income = 2000000
    client_1.family_income = 3000000
    client_1.save()

    blacklisted_client = Clients.objects.get(id=2)
    BlackLists.objects.create(client=blacklisted_client)

    credit = Credits.objects.create(
        client=blacklisted_client,
        credit_program=credit_programs[0],
        loan_size=1000000,
        period=12,
        init_payment=100000,
        interest_rate=10.0
    )

    for month in range(1, 5):
        payment_date = datetime.now() - timedelta(days=30 * month)
        payment = PaymentSchedules.objects.create(
            credit=credit,
            date=payment_date,
            main_payment_amount=credit.loan_size / credit.period,
            percents_payment_amount=(credit.loan_size * credit.interest_rate / 100) / 12,
            condition=PaymentConditions.objects.create(name="Просрочен")
        )
        PaymentDelays.objects.create(credit=credit, payment=payment)

    print("Test data created!")


if __name__ == "__main__":
    create_test_data()
