/**
 * Datepicker Initializer
 * Usa Flatpickr para agregar selectores de fecha y hora
 * a los campos DateField, TimeField y DateTimeField
 */

document.addEventListener('DOMContentLoaded', function() {
    // Configuración para campos DateField (solo fecha)
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        flatpickr(input, {
            mode: 'single',
            dateFormat: 'd/m/Y',
            locale: 'es',
            monthSelectorType: 'dropdown',
            yearSelectorType: 'dropdown',
            allowInput: true,
            yearRange: [1900, new Date().getFullYear() + 10]
        });
    });

    // Configuración para campos TimeField (solo hora)
    const timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(input => {
        flatpickr(input, {
            enableTime: true,
            noCalendar: true,
            dateFormat: 'H:i',
            time_24hr: true,
            allowInput: true,
            minuteIncrement: 1,
            static: true,
            inline: false
        });
    });

    // Configuración para campos DateTimeField (fecha y hora)
    const datetimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    datetimeInputs.forEach(input => {
        flatpickr(input, {
            enableTime: true,
            dateFormat: 'd/m/Y H:i',
            locale: 'es',
            monthSelectorType: 'dropdown',
            yearSelectorType: 'dropdown',
            yearRange: [1900, new Date().getFullYear() + 10],
            time_24hr: true,
            allowInput: true,
            minuteIncrement: 1
        });
    });

    // Para cualquier campo con clase 'date-picker'
    const customDatePickers = document.querySelectorAll('.date-picker');
    customDatePickers.forEach(input => {
        flatpickr(input, {
            mode: 'single',
            dateFormat: 'd/m/Y',
            locale: 'es',
            monthSelectorType: 'dropdown',
            yearSelectorType: 'dropdown',
            yearRange: [1900, new Date().getFullYear() + 10],
            allowInput: true
        });
    });

    // Para cualquier campo con clase 'time-picker'
    const customTimePickers = document.querySelectorAll('.time-picker');
    customTimePickers.forEach(input => {
        flatpickr(input, {
            enableTime: true,
            noCalendar: true,
            dateFormat: 'H:i',
            time_24hr: true,
            allowInput: true,
            minuteIncrement: 1,
            static: true,
            inline: false
        });
    });

    // Para cualquier campo con clase 'datetime-picker'
    const customDatetimePickers = document.querySelectorAll('.datetime-picker');
    customDatetimePickers.forEach(input => {
        flatpickr(input, {
            enableTime: true,
            dateFormat: 'd/m/Y H:i',
            locale: 'es',
            monthSelectorType: 'dropdown',
            yearSelectorType: 'dropdown',
            yearRange: [1900, new Date().getFullYear() + 10],
            time_24hr: true,
            allowInput: true,
            minuteIncrement: 1
        });
    });
});

