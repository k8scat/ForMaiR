package inbound

import (
	"log"

	"github.com/juju/errors"
	"github.com/k8scat/go-pop3"
)

type POP3InboundOptions struct {
	Host       string
	Port       int
	User       string
	Password   string
	TLSEnabled bool
	FetchIndex uint32
}

type POP3Inbound struct {
	opts     *POP3InboundOptions
	messages chan any
}

func NewPOP3Inbound(opts *POP3InboundOptions) *POP3Inbound {
	return &POP3Inbound{
		opts:     opts,
		messages: make(chan any, 10),
	}
}

func (in *POP3Inbound) Fetch() error {
	client := pop3.New(pop3.Opt{
		Host:          in.opts.Host,
		Port:          in.opts.Port,
		TLSEnabled:    in.opts.TLSEnabled,
		TLSSkipVerify: true,
	})

	c, err := client.NewConn()
	if err != nil {
		return errors.Trace(err)
	}
	defer c.Quit()

	if err = c.Auth(in.opts.User, in.opts.Password); err != nil {
		return errors.Trace(err)
	}

	count, _, err := c.Stat()
	if err != nil {
		return errors.Trace(err)
	}
	for id := int(in.opts.FetchIndex); id <= count; id++ {
		log.Printf("retr %d\n", id)
		msg, err := c.Retr(id)
		if err != nil {
			return errors.Trace(err)
		}
		in.messages <- msg
	}
	return nil
}

func (in *POP3Inbound) Messages() <-chan any {
	return in.messages
}

func (in *POP3Inbound) Close() error {
	close(in.messages)
	return nil
}

var _ Inbound = (*POP3Inbound)(nil)
