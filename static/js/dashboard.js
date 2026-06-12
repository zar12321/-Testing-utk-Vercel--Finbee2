document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "dashboard-filter-form"
            );

        if (!form) return;

        form.addEventListener(
            "submit",
            async (e) => {

                e.preventDefault();

                const month =
                    document.getElementById(
                        "filter-month"
                    ).value;

                const year =
                    document.getElementById(
                        "filter-year"
                    ).value;

                const response =
                    await fetch(
                        `/dashboard/data?month=${month}&year=${year}`
                    );

                const data =
                    await response.json();

                console.log(data);
            }
        );
    }
);