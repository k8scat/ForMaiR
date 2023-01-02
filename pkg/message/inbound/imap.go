package inbound

import (
	"log"
	"strconv"

	"github.com/emersion/go-imap"
	"github.com/emersion/go-imap/client"
	"github.com/juju/errors"
)

type IMAPInboundOptions struct {
	Host       string
	Port       int
	User       string
	Password   string
	TLSEnabled bool
	Mailbox    string
	FetchIndex uint32
	Step       uint32
}

type IMAPInbound struct {
	opts     *IMAPInboundOptions
	messages chan any
}

func NewIMAPInbound(opts *IMAPInboundOptions) *IMAPInbound {
	if opts.Step == 0 {
		opts.Step = 10
	}
	return &IMAPInbound{
		opts:     opts,
		messages: make(chan any, 10),
	}
}

func (in *IMAPInbound) Fetch() error {
	addr := in.opts.Host + ":" + strconv.Itoa(in.opts.Port)
	var c *client.Client
	var err error
	if in.opts.TLSEnabled {
		c, err = client.DialTLS(addr, nil)
	} else {
		c, err = client.Dial(addr)
	}
	if err != nil {
		return errors.Trace(err)
	}
	defer c.Logout()

	err = c.Login(in.opts.User, in.opts.Password)
	if err != nil {
		return errors.Trace(err)
	}

	mbox, err := c.Select(in.opts.Mailbox, true)
	if err != nil {
		return errors.Trace(err)
	}

	if in.opts.FetchIndex == 0 {
		in.opts.FetchIndex = 1
	}

	done := make(chan error, 1)
	defer close(done)
	for i := int(in.opts.FetchIndex); i <= int(mbox.Messages); {
		from := uint32(i)
		i += int(in.opts.Step)
		to := from + in.opts.Step
		log.Printf("Fetch from %d to %d", from, to)

		seqset := new(imap.SeqSet)
		seqset.AddRange(from, to)
		messages := make(chan *imap.Message, in.opts.Step*2)
		go func() {
			done <- c.Fetch(seqset, []imap.FetchItem{imap.FetchEnvelope, imap.FetchBody, imap.FetchRFC822}, messages)
		}()

		for msg := range messages {
			in.messages <- msg
		}
		if err = <-done; err != nil {
			return errors.Trace(err)
		}
	}
	return nil
}

func (in *IMAPInbound) Messages() <-chan any {
	return in.messages
}

func (in *IMAPInbound) Close() error {
	close(in.messages)
	return nil
}

var _ Inbound = (*IMAPInbound)(nil)
