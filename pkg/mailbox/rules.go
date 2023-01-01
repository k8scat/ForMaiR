package mailbox

import (
	"github.com/emersion/go-message"
	"log"
)

type EqualRule struct {
	key        string
	value      string
	recipients []string
}

func NewEqualRule(key, value string, recipients []string) *EqualRule {
	return &EqualRule{
		key:        key,
		value:      value,
		recipients: recipients,
	}
}

func (f EqualRule) Match(msg any) bool {
	switch v := msg.(type) {
	case *message.Entity:
		return v.Header.Get(f.key) == f.value
	}
	return false
}

func (f EqualRule) Send(msg any) error {
	log.Printf("send msg to %v: %+v", f.recipients, msg)
	return nil
}

var _ Rule = (*EqualRule)(nil)
