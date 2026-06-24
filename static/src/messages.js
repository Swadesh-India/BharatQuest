document.addEventListener("DOMContentLoaded", function () {
        const alertContainers = Array.from(
          document.querySelectorAll(".alert-container:not(.validation)"),
        );
        if (alertContainers) {
          setTimeout(() => {
            alertContainers.forEach((alertContainer) => {
              alertContainer.style.transition =
                "opacity 0.4s ease, transform 0.4s ease";
              alertContainer.style.opacity = "0";
              alertContainer.style.transform = "translateY(-10px)";

              setTimeout(() => {
                alertContainer.remove();
              }, 400);
            });
          }, 2000);
        }
      });
      
      
