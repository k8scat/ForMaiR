package outbound

import (
	"crypto/tls"
	"io"
	"net/smtp"
	"strconv"

	"github.com/jordan-wright/email"
	"github.com/juju/errors"
	"github.com/k8scat/go-message"
)

type SMTPOutboundOptions struct {
	Host       string
	Port       int
	User       string
	Password   string
	To         []string
	TLSEnabled bool
}

type SMTPOutbound struct {
	opts *SMTPOutboundOptions
}

func NewSMTPOutbound(opts *SMTPOutboundOptions) *SMTPOutbound {
	return &SMTPOutbound{
		opts: opts,
	}
}

const (
	contentTypeMultipartAlternative = "multipart/alternative"
	contentTypeMultipartMixed       = "multipart/mixed"
	contentTypeTextPlain            = "text/plain"
	contentTypeTextHTML             = "text/html"
)

func (out *SMTPOutbound) send(msg *message.Entity) error {
	e := email.NewEmail()
	e.From = out.opts.User
	e.To = out.opts.To
	e.Subject = msg.Header.Get("Subject")

	mr := msg.MultipartReader()
	if mr != nil {
		for {
			entity, err := mr.NextPart()
			if err != nil {
				if err == io.EOF {
					break
				}
				return errors.Trace(err)
			}

			t, _, err := entity.Header.ContentType()
			if err != nil {
				return errors.Trace(err)
			}
			switch t {
			case contentTypeTextPlain:
				b, err := io.ReadAll(entity.Body)
				if err != nil {
					return errors.Trace(err)
				}
				e.Text = b
			case contentTypeTextHTML:
				b, err := io.ReadAll(entity.Body)
				if err != nil {
					return errors.Trace(err)
				}
				e.HTML = b
			}
		}
	}

	addr := out.opts.Host + ":" + strconv.Itoa(out.opts.Port)
	auth := smtp.PlainAuth("", out.opts.User, out.opts.Password, out.opts.Host)
	var err error
	if out.opts.TLSEnabled {
		tlsConfig := &tls.Config{
			InsecureSkipVerify: true,
			ServerName:         out.opts.Host,
		}
		err = e.SendWithTLS(addr, auth, tlsConfig)
	} else {
		err = e.Send(addr, auth)
	}
	return errors.Trace(err)
}

func (out *SMTPOutbound) Send(msgs []any) error {
	for _, m := range msgs {
		switch v := m.(type) {
		case *message.Entity:
			if err := out.send(v); err != nil {
				return errors.Trace(err)
			}
		default:
			return errors.Errorf("invalid msg: %#v", v)
		}

	}
	return nil
}
