package forwarding

import (
	"github.com/k8scat/formair/pkg/message/inbound"
	"github.com/k8scat/formair/pkg/message/rule"
)

type Forwarding interface {
	inbound.Inbound

	AddRule(r rule.Rule) error
	Rules() ([]rule.Rule, error)

	Forwarding() error
}
