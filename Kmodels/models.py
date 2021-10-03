from django.db import models

from django.contrib.auth.models import User

from .clientModel import Client






class Transaction(models.Model):

    trans_date = models.DateTimeField(verbose_name="Date de transaction", auto_now_add=True)
    trans_amount = models.DecimalField(verbose_name="Montat de la transaction", max_digits=12, decimal_places=2)
    trans_cost = models.DecimalField(verbose_name="Coût de la transaction", max_digits=5, decimal_places=2, default=0)

    desc_type = models.CharField(verbose_name="Type ou description de la transaction", 
                max_length=250, default="Envoie")

    sender = models.ForeignKey(Client, verbose_name="Acteur de la transaction",
            related_name="client_senders", on_delete=models.CASCADE)
    recever = models.ForeignKey(Client, verbose_name="Bénéficiare", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.trans_date} - {self.trans_amount}"



class AgentSupply(Transaction):

    benefit = models.DecimalField(verbose_name="Interêt de recharge", max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{super().trans_date}  -  {super().trans_amount}  -  {self.benefit}"




class Bill(models.Model):

    bill_amount = models.DecimalField(verbose_name="Montat de la facture", max_digits=12, 
                    decimal_places=2)
    bill_submit_date = models.DateTimeField(verbose_name="Date de livraison", auto_now_add=True)
    is_payed = models.BooleanField(verbose_name="La facture est payer", default=False)

    bill_motif = models.CharField(max_length=250, verbose_name="Description")

    shop_assistant = models.ForeignKey(Client, verbose_name="Délivreur de la facture", on_delete=models.CASCADE)
    recipient = models.ForeignKey(Client, verbose_name="Bénéficiaire", 
                related_name="recipients", on_delete=models.CASCADE)
    transation = models.OneToOneField(Transaction, verbose_name="Paiement lier à la facture", 
                on_delete=models.CASCADE, blank=True, null=True)

    bill_payed_date = models.DateTimeField(verbose_name="Date de paiement", null=True, blank=True)


    def __str__(self):
        return f"{self.bill_submit_date} - {self.bill_amount} = {self.is_payed}"
