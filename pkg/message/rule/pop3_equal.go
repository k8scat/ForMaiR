package rule

import (
	"log"

	"github.com/k8scat/go-message"

	"github.com/k8scat/formair/pkg/message/outbound"
)

type POP3EqualRule struct {
	key   string
	value string

	outs []outbound.Outbound
}

func NewPOP3EqualRule(key, value string) *POP3EqualRule {
	return &POP3EqualRule{
		key:   key,
		value: value,
	}
}

func (f *POP3EqualRule) Match(msg any) bool {
	switch v := msg.(type) {
	case *message.Entity:
		return v.Header.Get(f.key) == f.value
	default:
		log.Printf("invalid msg: %#v", msg)
	}
	return false
}

func (f *POP3EqualRule) AddOutbound(out outbound.Outbound) error {
	f.outs = append(f.outs, out)
	return nil
}

func (f *POP3EqualRule) Outbounds() []outbound.Outbound {
	return f.outs
}

var _ Rule = (*POP3EqualRule)(nil)
