package inbound

type Inbound interface {
	Fetch() error
	Messages() <-chan any
	Close() error
}
