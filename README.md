Wrapper for Payfort system

Main object: PayFortObject
	__init__ takes  secret api key as parameter

Child objects:

	Customer (from payfort.customer)
		methods:
			-create,
			-get,
			-update,
			-all

	Card (from payfort.cards)
		methods:
			-create,
			-get,
			-delete,
			-all

	Charge (from payfort.charges)
		methods:
			-create,
			-get,
			-capture,
			-all)

		Capture a chard:
			This step only applies to Authorizations (i.e. charges originally created with capture=false)

	Refund (from payfort.refunds)
		methods:
			-create,
			-all

	Token (from payfort.tokens)
		methods:
			-create
