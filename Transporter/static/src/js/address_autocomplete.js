odoo.define('fleet.depot.address_autocomplete', function (require) {
    "use strict";

    const fieldRegistry = require('web.field_registry');
    const FieldChar = require('web.basic_fields').FieldChar;

    const AddressAutocomplete = FieldChar.extend({
        events: _.extend({}, FieldChar.prototype.events, {
            'input': '_onAddressInput',
        }),

        _onAddressInput: function (event) {
            const self = this;
            const query = this.$el.val();

            if (query.length < 3) {
                return; // Only search if the query is at least 3 characters
            }

            const GEOCODING_API_URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json";
            const apiKey = "YOUR_API_KEY"; // Replace with actual API key

            $.ajax({
                url: GEOCODING_API_URL,
                type: "GET",
                data: {
                    input: query,
                    key: apiKey,
                },
                success: function (response) {
                    if (response.status === 'OK') {
                        const suggestions = response.predictions.map(pred => pred.description);
                        // Display suggestions (implement a dropdown here if needed)
                        console.log("Suggestions:", suggestions);
                    } else {
                        self.do_warn('Error', 'No suggestions found.');
                    }
                },
                error: function () {
                    self.do_warn('Error', 'Failed to fetch address suggestions.');
                }
            });
        },
    });

    fieldRegistry.add('address_autocomplete', AddressAutocomplete);
    return AddressAutocomplete;
});
