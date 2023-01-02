package outbound

type Outbound interface {
	Send(msgs []any) error
}
