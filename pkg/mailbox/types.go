package mailbox

type Rule interface {
	Match(msg any) bool
	Send(msg any) error
}

type Mailbox interface {
	Fetch() error
	AddRule(Rule) error
	Rules() ([]Rule, error)
	Forwarding() error
}
