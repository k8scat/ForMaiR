package rule

import "github.com/k8scat/formair/pkg/message/outbound"

type MatchAllRule struct {
	outs []outbound.Outbound
}

func NewMatchAllRule() *MatchAllRule {
	return &MatchAllRule{}
}

func (m *MatchAllRule) Match(msg any) bool {
	return true
}

func (m *MatchAllRule) AddOutbound(out outbound.Outbound) error {
	m.outs = append(m.outs, out)
	return nil
}

func (m *MatchAllRule) Outbounds() []outbound.Outbound {
	return m.outs
}

var _ Rule = (*MatchAllRule)(nil)
