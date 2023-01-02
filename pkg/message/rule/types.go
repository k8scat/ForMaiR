package rule

import "github.com/k8scat/formair/pkg/message/outbound"

type Rule interface {
	Match(msg any) bool
	AddOutbound(out outbound.Outbound) error
	Outbounds() []outbound.Outbound
}
