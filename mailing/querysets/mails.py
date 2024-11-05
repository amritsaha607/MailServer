from mailing.models import MailItem


def filter_emails(ids: list | None, senders: list | None, receivers: list | None):
    mails = MailItem.objects

    # Filter by id
    if isinstance(ids, list) and len(ids) > 0:
        mails = mails.filter(id__in=ids)

    # Filter by receivers
    if isinstance(receivers, list) and len(receivers) > 0:
        # receivers = [get_user_by_email(email) for email in receivers]
        mails = mails.filter(user__email__in=receivers)

    # Filter by senders
    if isinstance(senders, list) and len(senders) > 0:
        mails = mails.filter(event__sender__email__in=senders)

    return mails
