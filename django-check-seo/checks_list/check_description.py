# Standard Library
import re

# Third party
from django.utils.translation import gettext as _, ngettext, pgettext

# Local application / specific library imports
from ..checks import custom_list


def importance():
    """Scripts with higher importance will be executed in first.

    Returns:
        int -- Importance of the script.
    """
    return 1


def run(site):

    length_short = custom_list.CustomList(
        name=_("Meta description is too short"),
        settings=_("between {rule_low} and {rule_high} chars ").format(
            rule_low=site.settings.SEO_SETTINGS["meta_description_length"][0],
            rule_high=site.settings.SEO_SETTINGS["meta_description_length"][1],
        ),
        description=_(
            "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
        ),
    )

    length_long = custom_list.CustomList(
        name=_("Meta description is too long"),
        settings=_("between {rule_low} and {rule_high} chars ").format(
            rule_low=site.settings.SEO_SETTINGS["meta_description_length"][0],
            rule_high=site.settings.SEO_SETTINGS["meta_description_length"][1],
        ),
        description=_(
            "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
        ),
    )

    length_success = custom_list.CustomList(
        name=_("Meta description length is correct"),
        settings=_("between {rule_low} and {rule_high} chars ").format(
            rule_low=site.settings.SEO_SETTINGS["meta_description_length"][0],
            rule_high=site.settings.SEO_SETTINGS["meta_description_length"][1],
        ),
        description=_(
            "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
        ),
    )

    keywords_bad = custom_list.CustomList(
        name=_("No keyword in meta description"),
        settings=_("at least 1"),
        description=_(
            "The meta description tag can be displayed in search results, and the keywords present in the search will be in bold. All this can influence users, and Google ranks sites according to users behaviour."
        ),
    )

    keywords_good = custom_list.CustomList(
        name=_("Keywords were found in description"),
        settings=_("at least 1"),
        description=_(
            "The meta description tag can be displayed in search results, and the keywords present in the search will be in bold. All this can influence users, and Google ranks sites according to users behaviour."
        ),
    )

    too_much_meta = custom_list.CustomList(
        name=_("Too much meta description tags"),
        settings=_("only one"),
        description=_(
            "Although some people write a meta description by targeted keyword, this is still an uncommon practice that is not yet recognized by all search engines."
        ),
    )

    meta_description_only_one = custom_list.CustomList(
        name=_("Only one meta description tag"),
        settings=_("only one"),
        found=pgettext("description", "one"),
        description=_(
            "Although some people write a meta description by targeted keyword, this is still an uncommon practice that is not yet recognized by all search engines."
        ),
    )

    no_meta_description = custom_list.CustomList(
        name=_("No meta description"),
        settings=_("needed"),
        found=pgettext("description", "none"),
        description=_(
            "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
        ),
    )

    meta_description_present = custom_list.CustomList(
        name=_("Meta description is present"),
        settings=_("needed"),
        found=pgettext("description", "one"),
        description=_(
            "The meta description tag can be displayed in search results if it has the right length, and can influence users. Knowing that Google classifies sites according to user behaviour, it is important to have a relevant description."
        ),
    )

    meta = site.soup.find_all("meta")
    found_meta_description = False
    number_meta_description = 0

    for tag in meta:
        if (
            "name" in tag.attrs
            and tag.attrs["name"] == "description"
            and "content" in tag.attrs
            and tag.attrs["content"] != ""
        ):
            number_meta_description += 1
            found_meta_description = True

            length = len(tag.attrs["content"])

            # too short
            if length < site.settings.SEO_SETTINGS["meta_description_length"][0]:

                length_short.found = ngettext(
                    "%(words)d char", "%(words)d chars", length
                ) % {"words": length}
                site.problems.append(length_short)

            # too long
            elif length > site.settings.SEO_SETTINGS["meta_description_length"][1]:

                length_long.found = str(length)
                site.problems.append(length_long)

            # perfect
            else:

                length_success.found = str(length)
                site.success.append(length_success)

            occurence = []
            for keyword in site.keywords:
                occurence.append(
                    sum(
                        1
                        for _ in re.finditer(
                            r"\b%s\b" % re.escape(keyword.lower()),
                            tag.attrs["content"].lower(),
                        )
                    )
                )
            # if no keyword is found in h1
            print(occurence)
            if not any(i > 0 for i in occurence):

                keywords_bad.found = 0
                site.warnings.append(keywords_bad)

            # perfect
            else:

                keywords_good.found = max(i for i in occurence)
                site.success.append(keywords_good)

    # too many meta description
    if number_meta_description > 1:

        too_much_meta.found = number_meta_description
        site.warnings.append(too_much_meta)

    # perfect
    else:
        site.success.append(meta_description_only_one)

    # no meta description
    if not found_meta_description:
        site.problems.append(no_meta_description)

    # perfect
    else:
        site.success.append(meta_description_present)
