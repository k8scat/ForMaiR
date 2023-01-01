package mailbox

import (
	"fmt"
	"github.com/emersion/go-message"
	"github.com/knadh/go-pop3"
	"log"
)

type POP3 struct {
	user     string
	password string

	client   *pop3.Client
	messages chan *message.Entity

	rules []Rule
}

func NewPOP3(client *pop3.Client, user, password string) *POP3 {
	return &POP3{
		client:   client,
		user:     user,
		password: password,
		messages: make(chan *message.Entity, 10),
	}

}

func (p *POP3) Fetch() error {
	c, err := p.client.NewConn()
	if err != nil {
		return err
	}
	defer c.Quit()

	if err = c.Auth(p.user, p.password); err != nil {
		return err
	}
	count, _, err := c.Stat()
	if err != nil {
		return err
	}
	fmt.Printf("msg count: %d\n", count)
	for id := 1; id <= count; id++ {
		fmt.Printf("retr %d\n", id)
		m, err := c.Retr(id)
		if err != nil {
			return err
		}
		p.messages <- m
	}
	return nil
}

func (p *POP3) AddRule(rule Rule) error {
	p.rules = append(p.rules, rule)
	return nil
}

func (p *POP3) Rules() ([]Rule, error) {
	return p.rules, nil
}

func (p *POP3) Forwarding() error {
	for m := range p.messages {
		for _, r := range p.rules {
			if r.Match(m) {
				go func() {
					if err := r.Send(m); err != nil {
						log.Printf("rule send failed: %+v", err)
					}
				}()
			}
		}
	}
	return nil
}

var _ Mailbox = (*POP3)(nil)
