package mailbox

type IMAP struct{}

func (I IMAP) Fetch() error {
	//TODO implement me
	panic("implement me")
}

func (I IMAP) AddRule(rule Rule) error {
	//TODO implement me
	panic("implement me")
}

func (I IMAP) Rules() ([]Rule, error) {
	//TODO implement me
	panic("implement me")
}

func (I IMAP) Forwarding() error {
	//TODO implement me
	panic("implement me")
}

var _ Mailbox = (*IMAP)(nil)
