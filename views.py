class SendMoneyView(TransactionCreateMixin):
    form_class = SendMoneyForm
    template_name = "./transactions/sendmoney.html"
    title = "Send Money"
    success_url = reverse_lazy("transaction_report")

    def get_initial(self):
        initial = {"transaction_type": SEND_MONEY}
        return initial

    def form_valid(self, form):
        account_no = form.cleaned_data.get("account_no")
        amount = form.cleaned_data.get("amount")
        sender = self.request.user.account

        try:
            reciver = UserBankAccount.objects.get(account_no=account_no)
            reciver.balance += amount
            sender.balance -= amount
            reciver.save(update_fields=["balance"])
            sender.save(update_fields=["balance"])
            messages.success(self.request, "Send Money Successful")
            send_transaction_email(
                self.request.user,
                amount,
                "Send Money",
                "transactions/sendmoney_email.html",
            )
            send_transaction_email(
                reciver.user,
                amount,
                "Receive Money",
                "transactions/receivemoney_email.html",
            )

            return super().form_valid(form)
        except UserBankAccount.DoesNotExist:
            form.add_error("account_no", "Invalid Account No")
            return super().form_invalid(form)


class PassChangeView(LoginRequiredMixin, FormView):
    form_class = PasswordChangeForm
    template_name = "./accounts/pass_change.html"
    success_url = reverse_lazy("profile")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Password Updated Successfully")
        send_transaction_email(
            self.request.user,
            "amount",
            "Password Change Notification",
            "./accounts/password_change_email.html",
        )
        return super().form_valid(form)
