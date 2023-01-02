package main

import (
	"log"

	"github.com/juju/errors"

	"github.com/k8scat/formair/pkg/message/forwarding"
	"github.com/k8scat/formair/pkg/message/inbound"
	"github.com/k8scat/formair/pkg/message/outbound"
	"github.com/k8scat/formair/pkg/message/rule"
)

func main() {
	user := ""
	password := ""
	to := []string{"k8scat@gmail.com"}

	inOpts := &inbound.IMAPInboundOptions{
		Host:       "imap.qq.com",
		Port:       993,
		User:       user,
		Password:   password,
		TLSEnabled: true,
		FetchIndex: 4,
		Mailbox:    "INBOX",
	}
	in := inbound.NewIMAPInbound(inOpts)
	f := forwarding.NewDefaultForwarding(in)

	outOpts := &outbound.SMTPOutboundOptions{
		Host:       "smtp.qq.com",
		Port:       465,
		User:       user,
		Password:   password,
		To:         to,
		TLSEnabled: true,
	}
	out := outbound.NewSMTPOutbound(outOpts)

	r := rule.NewPOP3EqualRule("From", "GitHub <notifications@github.com>")
	r.AddOutbound(out)

	f.AddRule(r)

	err := f.Forwarding()
	if err != nil {
		log.Fatalf("%+v", errors.Trace(err))
	}
}
