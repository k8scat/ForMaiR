package forwarding

import (
	"github.com/juju/errors"

	"github.com/k8scat/formair/pkg/message/inbound"
	"github.com/k8scat/formair/pkg/message/rule"
)

type DefaultForwarding struct {
	inbound.Inbound
	rules []rule.Rule
}

func NewDefaultForwarding(in inbound.Inbound) *DefaultForwarding {
	return &DefaultForwarding{Inbound: in}
}

func (f *DefaultForwarding) AddRule(r rule.Rule) error {
	f.rules = append(f.rules, r)
	return nil
}

func (f *DefaultForwarding) Rules() ([]rule.Rule, error) {
	return f.rules, nil
}

func (f *DefaultForwarding) Forwarding() error {
	defer f.Close()

	done := make(chan error, 1)
	go func() {
		done <- f.Fetch()
	}()
	for m := range f.Messages() {
		for _, r := range f.rules {
			if r.Match(m) {
				for _, out := range r.Outbounds() {
					if err := out.Send([]any{m}); err != nil {
						return errors.Trace(err)
					}
				}
			}
		}
	}
	err := <-done
	return errors.Trace(err)
}

var _ Forwarding = (*DefaultForwarding)(nil)
