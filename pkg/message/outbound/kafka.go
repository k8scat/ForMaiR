package outbound

type Kafka struct {
	brokers []string
	topic   string
}

func (k Kafka) Send(msgs []any) error {
	return nil
}

var _ Outbound = (*Kafka)(nil)
